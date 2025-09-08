# 🚀 GiftNest E-commerce Platform - Easy Deployment Guide

## ⚡ One-Command Setup

This project is designed for **super easy deployment** on any laptop with just **ONE COMMAND**!

### 🖥️ For Windows Users:
```bash
# Simply double-click this file:
SETUP.bat

# OR run in command prompt:
python setup.py
```

### 🐧 For Linux/Mac Users:
```bash
# Run this command:
./SETUP.sh

# OR alternatively:
python3 setup.py
```

## 📋 What Happens Automatically

The setup script will automatically:

1. ✅ **Check Python version** (requires Python 3.8+)
2. ✅ **Create virtual environment**
3. ✅ **Install all required packages**
4. ✅ **Setup environment configuration**
5. ✅ **Create database and run migrations**
6. ✅ **Collect static files**
7. ✅ **Create helper scripts for easy usage**

## 🎯 After Setup is Complete

### Start the Server:
- **Windows**: Double-click `run_server.bat`
- **Linux/Mac**: Run `./run_server.sh`

### Create Admin User:
- **Windows**: Double-click `create_superuser.bat`
- **Linux/Mac**: Run `./create_superuser.sh`

### Access the Platform:
- **Main Website**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🔧 Configuration

### Payment Gateway Setup (Optional):
Edit the `.env` file to add your payment credentials:

```env
# Razorpay (Currently Active)
RAZORPAY_ENABLED=True
RAZORPAY_KEY_ID=your_actual_key_here
RAZORPAY_KEY_SECRET=your_actual_secret_here
```

## 🛠️ Manual Setup (If Needed)

If you prefer manual setup:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install packages
pip install -r requirements.txt

# 4. Setup database
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

## 📁 Project Structure

```
gift_shop/
├── 🚀 SETUP.bat          # Windows one-command setup
├── 🚀 SETUP.sh           # Linux/Mac one-command setup
├── 🔧 setup.py           # Main setup script
├── ▶️ run_server.bat/sh   # Easy server startup
├── 👤 create_superuser.* # Easy admin creation
├── ⚙️ .env               # Configuration file
├── 📋 requirements.txt   # Python packages
├── 🎁 GiftNest Platform  # Your e-commerce site
└── 📚 docs/              # Documentation
```

## 🎉 Features Ready to Use

- ✅ **Product Management** - Add, edit, delete products
- ✅ **Shopping Cart** - Add products, update quantities
- ✅ **User Authentication** - Register, login, profiles
- ✅ **Order Management** - Track orders, order history
- ✅ **Payment Integration** - Razorpay ready (test mode)
- ✅ **Admin Panel** - Complete backend management
- ✅ **Responsive Design** - Works on all devices

## 🆘 Troubleshooting

### If setup fails:
1. **Check Python version**: Must be 3.8 or higher
2. **Check internet connection**: Required for package downloads
3. **Run as administrator**: On Windows, if permission issues
4. **Check antivirus**: Some antivirus may block script execution

### Common Issues:
- **"Python not found"**: Install Python 3.8+ from python.org
- **"Permission denied"**: Run terminal as administrator
- **"Package installation failed"**: Check internet connection

## 📞 Support

If you need help:
1. Check the error messages in the terminal
2. Ensure Python 3.8+ is installed
3. Make sure you're in the correct project directory
4. Try running the manual setup commands

---

## 🎯 Quick Start Summary

**For the fastest deployment:**

1. **Ensure Python 3.8+ is installed**
2. **Download the project**
3. **Double-click SETUP.bat (Windows) or run ./SETUP.sh (Linux/Mac)**
4. **Wait for setup to complete**
5. **Double-click run_server.bat (Windows) or run ./run_server.sh (Linux/Mac)**
6. **Open http://127.0.0.1:8000/ in your browser**

**That's it! Your e-commerce platform is ready! 🎉**