# 🚀 Deploy GiftNest to Render - Complete Guide

This guide will walk you through deploying your GiftNest e-commerce platform to [Render](https://render.com), a modern cloud platform that offers free hosting for web applications.

## 📋 Prerequisites

- A [GitHub](https://github.com) account
- A [Render](https://render.com) account (free)
- Your GiftNest project pushed to GitHub
- Payment gateway accounts (Razorpay/Stripe) for live payments

## 🔧 Pre-Deployment Setup

### 1. Push Your Code to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit - GiftNest e-commerce platform"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/giftnest.git

# Push to GitHub
git push -u origin main
```

### 2. Verify Required Files

Ensure these files are in your project root:
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `build.sh` - Build script
- ✅ Updated `gift_shop/settings.py` - Production settings

## 🌐 Render Deployment Steps

### Step 1: Create a New Web Service

1. **Login to Render Dashboard**
   - Go to [https://render.com](https://render.com)
   - Click "Get Started for Free" or "Login"
   - Connect your GitHub account if not already connected

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Choose "Build and deploy from a Git repository"
   - Click "Next"

3. **Connect Your Repository**
   - Select your GitHub account
   - Find and select your GiftNest repository
   - Click "Connect"

### Step 2: Configure Service Settings

**Basic Configuration:**
- **Name**: `giftnest` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn gift_shop.wsgi:application`

**Plan:**
- Select "Free" for testing
- Upgrade to "Starter" or higher for production

### Step 3: Add PostgreSQL Database

1. **Create Database Service**
   - Go back to Render Dashboard
   - Click "New +" button
   - Select "PostgreSQL"
   - **Name**: `giftnest-db`
   - **Database Name**: `giftnest_db`
   - **User**: `giftnest_user`
   - **Region**: Same as your web service
   - **Plan**: Free (for testing)

2. **Copy Database URL**
   - Once created, go to your database dashboard
   - Copy the "External Database URL"

### Step 4: Configure Environment Variables

In your web service dashboard, go to "Environment" tab and add:

**Essential Variables:**
```
SECRET_KEY=<generate-a-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=<paste-your-database-url>
```

**Payment Gateway Variables:**
```
RAZORPAY_KEY_ID=<your-live-key>
RAZORPAY_KEY_SECRET=<your-live-secret>
RAZORPAY_ENABLED=true
DEFAULT_PAYMENT_GATEWAY=razorpay
DEFAULT_CURRENCY=INR
```

**UPI Settings:**
```
UPI_ENABLED=true
UPI_VPA=your-business@upi
UPI_PAYEE_NAME=Your Business Name
```

> 📝 **Note**: See `RENDER_ENV_VARS.md` for complete list of environment variables

### Step 5: Deploy

1. **Trigger Deployment**
   - Click "Manual Deploy" → "Deploy Latest Commit"
   - Or push changes to your GitHub repository (auto-deploy)

2. **Monitor Build Process**
   - Watch the build logs in real-time
   - Build typically takes 2-5 minutes

3. **Verify Deployment**
   - Once build completes, click on your app URL
   - Verify the site loads correctly

## ✅ Post-Deployment Verification

### 1. Access Your Site
- **Main Site**: `https://your-app-name.onrender.com`
- **Admin Panel**: `https://your-app-name.onrender.com/admin/`

### 2. Admin Access
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@giftnest.com`

> 🚨 **Security**: Change the admin password immediately after first login!

### 3. Test Core Features
- [ ] Product catalog loading
- [ ] User registration/login
- [ ] Shopping cart functionality
- [ ] Order creation
- [ ] Payment processing (test mode first)
- [ ] Admin panel access

## 🔧 Configuration & Customization

### Custom Domain (Optional)

1. **Add Custom Domain in Render**
   - Go to "Settings" → "Custom Domains"
   - Add your domain (e.g., `www.yourdomain.com`)

2. **Update DNS Settings**
   - Add CNAME record pointing to your Render app
   - Update `ALLOWED_HOSTS` environment variable

3. **SSL Certificate**
   - Render automatically provides SSL certificates
   - Certificate provisioning may take a few minutes

### Payment Gateway Setup

#### For Razorpay (India):
1. Get live API keys from [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Update environment variables with live keys
3. Configure webhook URLs in Razorpay dashboard

#### For Stripe (International):
1. Get live API keys from [Stripe Dashboard](https://dashboard.stripe.com/)
2. Set `STRIPE_ENABLED=true` and `RAZORPAY_ENABLED=false`
3. Update `DEFAULT_PAYMENT_GATEWAY=stripe`

### Email Configuration

For transactional emails (order confirmations, etc.):
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📊 Monitoring & Maintenance

### Logs
- Monitor application logs in Render dashboard
- Check for errors and performance issues

### Database Management
- Use Render's database dashboard for basic management
- Consider database backups for production data

### Updates
- Push changes to GitHub to trigger automatic deployments
- Test changes in a staging environment first

## 🚨 Troubleshooting

### Common Issues

**Build Failures:**
- Check `build.sh` permissions and syntax
- Verify all dependencies in `requirements.txt`
- Check Python version compatibility

**500 Internal Server Error:**
- Verify `DEBUG=False` and correct `ALLOWED_HOSTS`
- Check database connectivity
- Review application logs

**Static Files Not Loading:**
- Verify WhiteNoise middleware configuration
- Check `STATIC_ROOT` setting
- Ensure `collectstatic` runs successfully

**Payment Issues:**
- Verify live API keys are correct
- Check webhook configurations
- Test in sandbox mode first

### Getting Help

1. **Render Documentation**: [https://render.com/docs](https://render.com/docs)
2. **Django Documentation**: [https://docs.djangoproject.com](https://docs.djangoproject.com)
3. **Check Application Logs**: Render Dashboard → Your Service → Logs

## 🎉 Success!

Once deployed, your GiftNest e-commerce platform will be live and accessible to users worldwide! 

### Next Steps:
1. Change default admin password
2. Add your products through admin panel
3. Configure payment gateways with live credentials
4. Set up monitoring and analytics
5. Create regular database backups
6. Consider CDN for faster static file delivery

---

## 📞 Support

If you encounter issues during deployment:
1. Check the troubleshooting section above
2. Review Render logs for specific error messages
3. Ensure all environment variables are correctly set
4. Verify your payment gateway configurations

**Happy Selling! 🛍️**