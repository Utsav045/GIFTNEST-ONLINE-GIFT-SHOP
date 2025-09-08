# Payment Integration Guide - GiftNest E-commerce Platform

## Overview

This document provides a complete guide to the multi-payment gateway integration in GiftNest, supporting both Razorpay and Stripe payment methods.

## Current Payment Options Detected

### 1. **Original System (Before Integration)**
- **Stripe Integration**: Present but disabled
- **Payment Flow**: Single gateway approach
- **Status**: Required real payment gateway configuration
- **Limitations**: No payment method selection, single currency support

### 2. **New Integrated System (After Integration)**
- **Razorpay Integration**: Full implementation with Indian market focus
- **Stripe Integration**: Enhanced and maintained
- **Payment Flow**: Multi-gateway selection system
- **Error Handling**: Proper validation when no gateways configured

## Supported Payment Gateways

### 🇮🇳 **Razorpay** (Primary - Indian Market)
- **Currencies**: INR (Indian Rupee)
- **Payment Methods**: 
  - Credit/Debit Cards (Visa, MasterCard, RuPay)
  - UPI (Google Pay, PhonePe, Paytm, etc.)
  - Net Banking (All major Indian banks)
  - Digital Wallets (Paytm, Mobikwik, etc.)
  - EMI Options
- **Features**: 
  - Real-time payment verification
  - Webhook support for automatic order updates
  - Mobile-optimized checkout
  - Support for recurring payments

### 🌍 **Stripe** (International Market)
- **Currencies**: USD, EUR, GBP (configurable)
- **Payment Methods**:
  - Credit/Debit Cards (Visa, MasterCard, Amex)
  - Digital Wallets (Apple Pay, Google Pay)
  - SEPA, ACH transfers
- **Features**:
  - Hosted checkout pages
  - Strong customer authentication (SCA)
  - Comprehensive fraud protection
  - Global payment method support


## Configuration Setup

### Environment Variables (.env file)

```env
# Django Core Settings
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Razorpay Configuration
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret_key
RAZORPAY_WEBHOOK_SECRET=your_razorpay_webhook_secret
RAZORPAY_ENABLED=True

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_stripe_webhook_secret
STRIPE_ENABLED=False

# Payment Gateway Settings
DEFAULT_PAYMENT_GATEWAY=razorpay  # 'razorpay' or 'stripe'
DEFAULT_CURRENCY=INR              # 'INR', 'USD', 'EUR', 'GBP'

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

### Getting API Keys

#### Razorpay Setup
1. **Sign up**: Visit [razorpay.com](https://razorpay.com) and create an account
2. **Business Verification**: Complete KYC and business verification
3. **API Keys**: Navigate to Settings > API Keys
   - Copy `Key ID` (starts with `rzp_test_` or `rzp_live_`)
   - Copy `Key Secret`
4. **Webhook**: Settings > Webhooks
   - URL: `https://yourdomain.com/payment/webhook/razorpay/`
   - Events: `payment.captured`, `payment.failed`
   - Copy webhook secret

#### Stripe Setup
1. **Sign up**: Visit [stripe.com](https://stripe.com) and create an account
2. **API Keys**: Dashboard > Developers > API Keys
   - Copy `Publishable Key` (starts with `pk_test_` or `pk_live_`)
   - Copy `Secret Key` (starts with `sk_test_` or `sk_live_`)
3. **Webhook**: Dashboard > Developers > Webhooks
   - URL: `https://yourdomain.com/payment/webhook/stripe/`
   - Events: `checkout.session.completed`
   - Copy webhook secret

## Payment Flow Architecture

### 1. **Payment Method Selection**
```
User places order → Payment method selection page → Gateway-specific processing
```

### 2. **Processing Flow**
```
Order Creation → Method Selection → Gateway Processing → Payment Verification → Order Completion
```

### 3. **URL Structure**
- `/payment/process/{order_id}/` - Payment method selection
- `/payment/process/{order_id}/?method=razorpay` - Razorpay processing
- `/payment/process/{order_id}/?method=stripe` - Stripe processing
- `/payment/success/{order_id}/?method={gateway}` - Success page
- `/payment/cancel/{order_id}/` - Cancellation page
- `/payment/verify/razorpay/` - Razorpay payment verification
- `/payment/webhook/razorpay/` - Razorpay webhook handler
- `/payment/webhook/stripe/` - Stripe webhook handler

## File Structure

```
payment/
├── views.py                 # Payment processing logic
├── urls.py                  # URL routing
├── models.py               # Payment models (if needed)
└── templates/payment/
    ├── select_method.html   # Payment method selection
    ├── razorpay_process.html # Razorpay payment form
    ├── stripe_process.html   # Stripe payment form
    ├── success.html         # Payment success page
    ├── cancel.html          # Payment cancellation
    └── no_methods.html      # No payment methods available
```

## Key Features Implemented

### ✅ **Multi-Gateway Support**
- Automatic gateway detection based on configuration
- Dynamic payment method selection
- Proper error handling when no gateways configured

### ✅ **Security Features**
- Webhook signature verification
- CSRF protection on all forms
- Secure payment verification
- Environment-based configuration

### ✅ **User Experience**
- Mobile-responsive payment forms
- Loading states and progress indicators
- Clear payment method descriptions
- Comprehensive error handling

### ✅ **Developer Experience**
- Comprehensive logging
- Easy configuration via environment variables
- Modular architecture for easy extension
- Comprehensive error handling

## Testing the Integration

### 1. **Razorpay Testing**
```bash
# Enable Razorpay with test keys
RAZORPAY_ENABLED=True
RAZORPAY_KEY_ID=rzp_test_...

# Test with Razorpay test card numbers
Card: 4111 1111 1111 1111
CVV: 123
Expiry: Any future date
```

### 2. **Stripe Testing**
```bash
# Enable Stripe with test keys
STRIPE_ENABLED=True
STRIPE_SECRET_KEY=sk_test_...

# Test with Stripe test card numbers
Card: 4242 4242 4242 4242
CVV: 123
Expiry: Any future date
```

## Production Deployment

### 1. **Security Checklist**
- [ ] Use HTTPS for all payment pages
- [ ] Set `DEBUG=False` in production
- [ ] Use production API keys (live keys)
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Set up proper webhook URLs
- [ ] Enable logging for payment transactions

### 2. **Performance Optimization**
- Use Redis/Celery for webhook processing
- Implement payment retry mechanisms
- Set up monitoring for payment failures
- Configure proper database indexing

### 3. **Compliance**
- Ensure PCI DSS compliance
- Implement proper data encryption
- Set up audit trails for payments
- Configure proper backup procedures

## Troubleshooting

### Common Issues

1. **\"No payment methods available\"**
   - Check environment variables are loaded
   - Verify API keys are correct
   - Ensure at least one gateway is enabled

2. **Razorpay payment verification fails**
   - Check webhook secret is correct
   - Verify signature verification logic
   - Check network connectivity

3. **Stripe redirect fails**
   - Verify publishable key is correct
   - Check success/cancel URLs are accessible
   - Ensure webhook endpoint is reachable

### Debug Commands

```bash
# Check Django configuration
python manage.py check

# Test payment gateway connectivity
python manage.py shell
>>> from payment.views import razorpay_client
>>> print(razorpay_client)

# Check webhook endpoints
curl -X POST http://localhost:8000/payment/webhook/razorpay/
```

## Support and Maintenance

For ongoing support:
1. Monitor payment success rates
2. Keep payment gateway SDKs updated
3. Regularly test payment flows
4. Monitor webhook delivery success
5. Keep security certificates updated

## Conclusion

The integrated payment system provides a robust, secure, and user-friendly solution for processing payments in the GiftNest e-commerce platform. It supports multiple payment gateways, handles various currencies, and provides comprehensive error handling and security features.

The system is designed to be easily maintainable and extensible, allowing for future payment method integrations with minimal code changes."