import stripe
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from orders.models import Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import hmac
import hashlib
import logging
from utils.emails import send_payment_confirmation

logger = logging.getLogger(__name__)

# Initialize payment gateways
if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY

if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
else:
    razorpay_client = None

def get_available_payment_methods():
    """Get list of available payment methods based on configuration"""
    methods = []
    # Cash on Delivery is always available as an offline option
    methods.append({
        'id': 'cod',
        'name': 'Cash on Delivery',
        'description': 'Pay with cash upon delivery',
        'logo': '',
        'currencies': []
    })
    # Manual UPI as fallback
    if getattr(settings, 'UPI_ENABLED', False) and settings.UPI_VPA:
        methods.append({
            'id': 'upi',
            'name': 'UPI (Manual)',
            'description': f"Pay to {getattr(settings, 'UPI_VPA', '')}",
            'logo': '',
            'currencies': ['INR']
        })
    
    if getattr(settings, 'RAZORPAY_ENABLED', False) and settings.RAZORPAY_KEY_ID:
        methods.append({
            'id': 'razorpay',
            'name': 'Razorpay',
            'description': 'Pay with UPI, Cards, Net Banking & more',
            'logo': 'https://razorpay.com/assets/razorpay-logo.svg',
            'currencies': ['INR']
        })
    
    if getattr(settings, 'STRIPE_ENABLED', False) and settings.STRIPE_SECRET_KEY:
        methods.append({
            'id': 'stripe',
            'name': 'Stripe',
            'description': 'Pay with Credit/Debit Cards worldwide',
            'logo': 'https://stripe.com/img/v3/newsroom/logos/stripe_logo_white.png',
            'currencies': ['USD', 'EUR', 'GBP']
        })
    
    return methods

@login_required
def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, paid=False)
    available_methods = get_available_payment_methods()
    
    # Check if any payment methods are available
    if not available_methods:
        messages.error(request, 'No payment methods are currently available. Please contact support.')
        return render(request, 'payment/no_methods.html', {'order': order})
    
    # If no payment method is selected, show selection page
    payment_method = request.GET.get('method') or request.POST.get('payment_method')
    
    if not payment_method:
        return render(request, 'payment/select_method.html', {
            'order': order,
            'payment_methods': available_methods
        })
    
    # Handle Razorpay payment
    if payment_method == 'razorpay':
        return handle_razorpay_payment(request, order)
    
    # Handle Stripe payment
    if payment_method == 'stripe':
        return handle_stripe_payment(request, order)
    
    # Handle Cash on Delivery (offline)
    if payment_method == 'cod':
        messages.success(request, 'Cash on Delivery selected. Your order will be processed and payable upon delivery.')
        # Keep order.paid as False for COD. Redirect to success page showing COD as the method.
        success_url = f"/payment/success/{order.id}/?method=cod"
        return redirect(success_url)

    # Handle manual UPI
    if payment_method == 'upi':
        return render(request, 'payment/upi_manual.html', {
            'order': order,
            'upi_vpa': getattr(settings, 'UPI_VPA', ''),
            'upi_name': getattr(settings, 'UPI_PAYEE_NAME', 'GiftNest')
        })
    
    messages.error(request, 'Invalid payment method selected.')
    return redirect('payment:process', order_id=order.id)

def handle_razorpay_payment(request, order):
    """Handle Razorpay payment processing"""
    if not razorpay_client:
        messages.error(request, 'Razorpay is not configured properly.')
        return redirect('payment:process', order_id=order.id)
    
    if request.method == 'POST':
        try:
            # Create Razorpay order
            razorpay_order = razorpay_client.order.create({
                'amount': int(order.get_total_cost() * 100),  # Amount in paise (INR * 100)
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': 1
            })
            
            # Update order with Razorpay order ID
            order.payment_intent_id = razorpay_order['id']
            order.save()
            
            return JsonResponse({
                'order_id': razorpay_order['id'],
                'amount': razorpay_order['amount'],
                'currency': razorpay_order['currency'],
                'key': settings.RAZORPAY_KEY_ID
            })
        except Exception as e:
            logger.error(f'Razorpay order creation failed: {str(e)}')
            messages.error(request, f'Payment processing error: {str(e)}')
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'payment/razorpay_process.html', {
        'order': order,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'currency': 'INR'
    })

def handle_stripe_payment(request, order):
    """Handle Stripe payment processing"""
    if not settings.STRIPE_SECRET_KEY:
        messages.error(request, 'Stripe is not configured properly.')
        return redirect('payment:process', order_id=order.id)
    
    if request.method == 'POST':
        try:
            success_url = request.build_absolute_uri(f'/payment/success/{order.id}/')
            cancel_url = request.build_absolute_uri(f'/payment/cancel/{order.id}/')

            session_data = {
                'mode': 'payment',
                'client_reference_id': order.id,
                'success_url': success_url,
                'cancel_url': cancel_url,
                'line_items': []
            }

            # Add order items to the Stripe checkout session
            for item in order.items.all():
                session_data['line_items'].append({
                    'price_data': {
                        'unit_amount': int(item.price * 100),  # amount in cents
                        'currency': getattr(settings, 'DEFAULT_CURRENCY', 'usd').lower(),
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                })

            # Create Stripe checkout session
            session = stripe.checkout.Session.create(**session_data)

            # Update order with payment intent
            order.payment_intent_id = session.payment_intent
            order.save()

            return JsonResponse({'sessionId': session.id})
        except Exception as e:
            logger.error(f'Stripe session creation failed: {str(e)}')
            messages.error(request, f'Payment processing error: {str(e)}')
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'payment/stripe_process.html', {
        'order': order,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment_method = request.GET.get('method', 'unknown')
    
    return render(request, 'payment/success.html', {
        'order': order,
        'payment_method': payment_method
    })

@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'payment/cancel.html', {'order': order})

@csrf_exempt
@require_http_methods(["POST"])
def razorpay_verify_payment(request):
    """Verify Razorpay payment after successful payment"""
    if not razorpay_client:
        return JsonResponse({'error': 'Razorpay not configured'}, status=400)
    
    try:
        data = json.loads(request.body)
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return JsonResponse({'error': 'Missing payment details'}, status=400)
        
        # Verify payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except:
            return JsonResponse({'error': 'Payment verification failed'}, status=400)
        
        # Find and update order
        try:
            order = Order.objects.get(payment_intent_id=razorpay_order_id)
            order.paid = True
            order.stripe_id = razorpay_payment_id  # Reuse this field for Razorpay payment ID
            order.save()
            # Send payment confirmation with invoice
            try:
                send_payment_confirmation(order)
            except Exception as e:
                logger.warning(f'Failed to send payment confirmation email: {str(e)}')
            
            logger.info(f'Razorpay payment verified for order {order.id}')
            return JsonResponse({'status': 'success', 'order_id': order.id})
            
        except Order.DoesNotExist:
            logger.error(f'Order not found for Razorpay order ID: {razorpay_order_id}')
            return JsonResponse({'error': 'Order not found'}, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.error(f'Razorpay verification error: {str(e)}')
        return JsonResponse({'error': 'Payment verification failed'}, status=500)

@csrf_exempt
def razorpay_webhook(request):
    """Handle Razorpay webhooks"""
    if not settings.RAZORPAY_WEBHOOK_SECRET:
        return HttpResponse(status=200)
    
    payload = request.body
    sig_header = request.META.get('HTTP_X_RAZORPAY_SIGNATURE', '')
    
    try:
        # Verify webhook signature
        expected_signature = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(sig_header, expected_signature):
            logger.warning('Invalid Razorpay webhook signature')
            return HttpResponse(status=400)
        
        # Process webhook event
        data = json.loads(payload)
        event_type = data.get('event')
        
        if event_type == 'payment.captured':
            payment_data = data.get('payload', {}).get('payment', {}).get('entity', {})
            order_id = payment_data.get('order_id')
            payment_id = payment_data.get('id')
            
            if order_id:
                try:
                    order = Order.objects.get(payment_intent_id=order_id)
                    order.paid = True
                    order.stripe_id = payment_id
                    order.save()
                    try:
                        send_payment_confirmation(order)
                    except Exception as e:
                        logger.warning(f'Failed to send payment confirmation email (webhook): {str(e)}')
                    logger.info(f'Razorpay webhook processed for order {order.id}')
                except Order.DoesNotExist:
                    logger.error(f'Order not found in webhook: {order_id}')
        
        return HttpResponse(status=200)
        
    except Exception as e:
        logger.error(f'Razorpay webhook error: {str(e)}')
        return HttpResponse(status=400)

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    # Skip webhook processing if Stripe is disabled
    if not getattr(settings, 'STRIPE_ENABLED', False) or not settings.STRIPE_SECRET_KEY:
        return HttpResponse(status=200)
    
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f'Invalid Stripe payload: {str(e)}')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f'Invalid Stripe signature: {str(e)}')
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        order_id = session.client_reference_id
        try:
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            logger.info(f'Stripe webhook processed for order {order.id}')
            try:
                send_payment_confirmation(order)
            except Exception as e:
                logger.warning(f'Failed to send Stripe payment confirmation email: {str(e)}')
        except Order.DoesNotExist:
            logger.error(f'Order not found in Stripe webhook: {order_id}')

    return HttpResponse(status=200)
