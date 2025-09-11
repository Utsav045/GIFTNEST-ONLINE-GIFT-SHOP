from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import OrderItem, Order
from cart.cart import Cart
from products.models import Product
from django.template.loader import render_to_string
from django.http import HttpResponse
import io
try:
    from xhtml2pdf import pisa  # type: ignore
except Exception:
    pisa = None

@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        # First, check stock availability for all items
        stock_errors = []
        for item in cart:
            product = item['product']
            if product.stock < item['quantity']:
                stock_errors.append(f"{product.name}: Only {product.stock} items available, but {item['quantity']} requested")
        
        if stock_errors:
            for error in stock_errors:
                messages.error(request, error)
            return render(request, 'orders/create.html', {'cart': cart})
        
        # Use transaction to ensure atomicity
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    address=request.POST['address'],
                    postal_code=request.POST['postal_code'],
                    city=request.POST['city']
                )
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                    # Reduce stock safely
                    product = item['product']
                    product.stock -= item['quantity']
                    product.save()
                cart.clear()
                messages.success(request, 'Order created successfully!')
                return redirect('payment:process', order_id=order.id)
        except Exception as e:
            messages.error(request, f'An error occurred while creating the order: {str(e)}')
            return render(request, 'orders/create.html', {'cart': cart})
    return render(request, 'orders/create.html', {
        'cart': cart
    })

@login_required
def order_detail(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})

@login_required
def order_invoice_pdf(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    html = render_to_string('orders/invoice.html', {'order': order}, request=request)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_order_{order.id}.pdf"'

    if pisa is None:
        return HttpResponse(html)
    result = io.BytesIO()
    pdf_status = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=result, encoding='utf-8')
    if pdf_status.err:
        return HttpResponse(html)
    response.write(result.getvalue())
    return response
