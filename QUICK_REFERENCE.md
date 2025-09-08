# 🎁 GiftNest E-commerce Platform - Quick Reference

## ⚡ One-Command Setup

### Windows:
```bash
SETUP.bat
```

### Linux/Mac:
```bash
./SETUP.sh
```

## 🚀 Daily Commands

### Start Server:
- **Windows**: `run_server.bat`
- **Linux/Mac**: `./run_server.sh`
- **Manual**: `python manage.py runserver`

### Create Admin User:
- **Windows**: `create_superuser.bat`
- **Linux/Mac**: `./create_superuser.sh`
- **Manual**: `python manage.py createsuperuser`

## 🌐 URLs

- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📁 Key Files

- **Configuration**: `.env`
- **Packages**: `requirements.txt`
- **Database**: `db.sqlite3`
- **Documentation**: `DEPLOYMENT_GUIDE.md`

## 💳 Payment Testing

### Razorpay Test Cards:
- **Card**: `4111 1111 1111 1111`
- **CVV**: Any 3 digits
- **Expiry**: Any future date

## 🔧 Troubleshooting

### Common Commands:
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install packages
pip install -r requirements.txt

# Database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

### If Setup Fails:
1. Check Python version (needs 3.8+)
2. Check internet connection
3. Run as administrator
4. Check antivirus settings

---
**Ready to launch your e-commerce platform! 🎉**