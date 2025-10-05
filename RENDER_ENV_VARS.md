# Environment Variables Configuration for Render Deployment

This document outlines all the environment variables you need to configure in your Render dashboard for the GiftNest e-commerce platform.

## Required Environment Variables

### Django Core Settings
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,your-custom-domain.com
```

### Database Configuration
```
DATABASE_URL=postgresql://user:password@host:port/database
```
*Note: This is automatically provided by Render when you add a PostgreSQL database service*

### Payment Gateway Settings

#### Razorpay (Recommended for Indian market)
```
RAZORPAY_KEY_ID=rzp_live_your_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret_key
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
RAZORPAY_ENABLED=true
```

#### Stripe (For international payments)
```
STRIPE_PUBLISHABLE_KEY=pk_live_your_publishable_key
STRIPE_SECRET_KEY=sk_live_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
STRIPE_ENABLED=false
```

### Payment Configuration
```
DEFAULT_PAYMENT_GATEWAY=razorpay
DEFAULT_CURRENCY=INR
```

### UPI Settings (India-specific)
```
UPI_ENABLED=true
UPI_VPA=your-business@upi
UPI_PAYEE_NAME=Your Business Name
```

### Email Configuration (Optional)
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## How to Set Environment Variables in Render

1. **Go to your Render Dashboard**
2. **Select your web service**
3. **Click on "Environment" tab**
4. **Add each variable one by one**:
   - Key: Variable name (e.g., `SECRET_KEY`)
   - Value: Variable value (e.g., your actual secret key)

## Security Best Practices

### Secret Key Generation
Generate a new secret key for production:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Payment Gateway Keys
- **Never use test keys in production**
- Get live keys from your payment provider's dashboard
- Razorpay: https://dashboard.razorpay.com/
- Stripe: https://dashboard.stripe.com/

### Domain Configuration
- Replace `your-app-name.onrender.com` with your actual Render app URL
- Add any custom domains you plan to use

## Testing the Configuration

After deployment, verify that:
1. The site loads without errors
2. Admin panel is accessible
3. Payment gateways are working
4. Static files are served correctly
5. Database connections are stable

## Troubleshooting

### Common Issues:
1. **500 Error**: Check DEBUG=False and ALLOWED_HOSTS
2. **Static files not loading**: Verify STATIC_ROOT and WhiteNoise configuration
3. **Database errors**: Check DATABASE_URL format
4. **Payment failures**: Verify live payment gateway credentials

### Logs
Check Render logs for detailed error messages:
1. Go to your service dashboard
2. Click on "Logs" tab
3. Look for error messages

## Production Checklist

- [ ] SECRET_KEY is set to a strong, unique value
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS includes your domain
- [ ] DATABASE_URL is configured
- [ ] Payment gateway live keys are set
- [ ] Email configuration is working (optional)
- [ ] SSL/HTTPS is enabled (automatic on Render)
- [ ] Static files are being served correctly