# 🎁 GiftNest E-commerce Platform

> A complete Django-based e-commerce platform for gift shopping with integrated payment processing, simplified UI, and comprehensive order management.

## ✨ Features

### 🛍️ **Core E-commerce Features**
- Product catalog with search and filtering
- Shopping cart with fixed quantity management
- User authentication and profiles
- Order management system
- Responsive design with Bootstrap 5

### 💳 **Payment Integration**
- **Razorpay** integration (UPI, Cards, Net Banking)
- **Stripe** support (International payments)
- Secure webhook handling
- Test mode with real payment gateway APIs

### 🎨 **User Experience**
- Simplified UI interfaces (Products, Cart, Checkout)
- Mobile-responsive design
- Clean and intuitive navigation
- Fixed cart quantity anomaly issues

### 🔒 **Security & Reliability**
- CSRF protection
- Stock validation before orders
- Secure payment verification
- Comprehensive error handling

## 🚀 Quick Start

### ⚡ **One-Command Setup** (Recommended)

For the **fastest deployment**, use our automated setup:

**Windows Users:**
```bash
# Simply double-click:
SETUP.bat
```

**Linux/Mac Users:**
```bash
# Run this command:
./SETUP.sh
```

**That's it! The script will automatically:**
- ✅ Create virtual environment
- ✅ Install all packages
- ✅ Setup database
- ✅ Create configuration files
- ✅ Setup helper scripts

### 🎯 **After Setup**
- **Start Server**: Double-click `run_server.bat` (Windows) or run `./run_server.sh` (Linux/Mac)
- **Create Admin**: Double-click `create_superuser.bat` (Windows) or run `./create_superuser.sh` (Linux/Mac)
- **Access Site**: http://127.0.0.1:8000/

### 🔧 **Manual Setup** (Alternative)
```bash
git clone <repository-url>
cd gift_shop
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### ⚙️ **Configuration**
Edit `.env` file for payment settings:
```env
# Payment Gateway (Razorpay - Active)
RAZORPAY_ENABLED=True
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

## 📋 Current Status

✅ **Payment Gateway**: Razorpay configured and working  
✅ **Products**: 9 products with proper pricing (₹800-₹3200)  
✅ **Cart System**: Fixed quantity update issues  
✅ **UI/UX**: Simplified interfaces implemented  
✅ **Security**: All validations and protections in place  

## 📚 Documentation

All detailed documentation is organized in the [`docs/`](./docs/) folder:

- **[🚀 Easy Deployment Guide](./DEPLOYMENT_GUIDE.md)** - One-command setup instructions
- **[Payment Integration Guide](./docs/PAYMENT_INTEGRATION_GUIDE.md)** - Complete payment setup
- **[Payment & Products Setup](./docs/PAYMENT_PRODUCTS_SETUP.md)** - Current configuration status
- **[Stock Management Fix](./docs/STOCK_MANAGEMENT_FIX.md)** - Database integrity fixes
- **[Demo Payment Removal](./docs/DEMO_PAYMENT_REMOVAL.md)** - Production-ready changes
- **[Error Fixes Summary](./docs/ERROR_FIXES_SUMMARY.md)** - All bugs fixed
- **[Template Error Fix](./docs/TEMPLATE_ERROR_FIX.md)** - UI/template improvements

## 🛠️ Project Structure

```
gift_shop/
├── docs/                    # 📚 All documentation
├── cart/                    # 🛒 Shopping cart functionality
├── orders/                  # 📦 Order processing
├── payment/                 # 💳 Payment gateway integration
├── products/                # 🎁 Product catalog
├── users/                   # 👤 User management
├── templates/               # 🎨 HTML templates
├── static/                  # 📁 CSS, JS, images
├── media/                   # 🖼️ Uploaded files
├── .env                     # ⚙️ Environment variables
├── requirements.txt         # 📋 Dependencies
└── manage.py               # 🚀 Django management
```

## 🧪 Testing

### **Run Tests**
```bash
python manage.py test
```

### **Test Payment Flow**
1. Add products to cart
2. Proceed to checkout
3. Use Razorpay test credentials:
   - **Card**: `4111 1111 1111 1111`
   - **CVV**: Any 3 digits
   - **Expiry**: Any future date

## 🔧 Production Deployment

For production deployment:
1. Replace test credentials with live payment keys
2. Configure production database
3. Set up HTTPS/SSL
4. Configure email backend
5. Set up static file serving

See [`docs/PAYMENT_INTEGRATION_GUIDE.md`](./docs/PAYMENT_INTEGRATION_GUIDE.md) for detailed production setup.

## 📞 Support

- **Issues**: Check [`docs/ERROR_FIXES_SUMMARY.md`](./docs/ERROR_FIXES_SUMMARY.md)
- **Setup**: See [`docs/PAYMENT_PRODUCTS_SETUP.md`](./docs/PAYMENT_PRODUCTS_SETUP.md)
- **Configuration**: Review [`.env.example`](./.env.example)

## 📄 License

This project is licensed under the MIT License.

---

**🎉 GiftNest is production-ready with working payment gateway and comprehensive e-commerce features!**
