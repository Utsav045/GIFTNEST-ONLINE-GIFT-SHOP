#!/usr/bin/env python
"""
GiftNest E-commerce Platform - Automated Setup Script
This script handles the complete setup of the GiftNest platform including:
- Virtual environment creation
- Package installation
- Database setup
- Initial configuration
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🎁 GiftNest E-commerce Platform - Automated Setup")
    print("=" * 60)

def check_python_version():
    """Check if Python 3.8+ is installed"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. You have Python {}.{}.{}".format(
            version.major, version.minor, version.micro))
        return False
    print("✅ Python {}.{}.{} detected".format(version.major, version.minor, version.micro))
    return True

def create_virtual_environment():
    """Create virtual environment"""
    print("\n🔧 Creating virtual environment...")
    try:
        venv.create('venv', with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print("❌ Failed to create virtual environment: {}".format(e))
        return False

def get_venv_python():
    """Get the path to the virtual environment Python executable"""
    if platform.system() == "Windows":
        return os.path.join('venv', 'Scripts', 'python.exe')
    else:
        return os.path.join('venv', 'bin', 'python')

def get_venv_pip():
    """Get the path to the virtual environment pip executable"""
    if platform.system() == "Windows":
        return os.path.join('venv', 'Scripts', 'pip.exe')
    else:
        return os.path.join('venv', 'bin', 'pip')

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        pip_path = get_venv_pip()
        subprocess.check_call([pip_path, 'install', '--upgrade', 'pip'])
        subprocess.check_call([pip_path, 'install', '-r', 'requirements.txt'])
        print("✅ All packages installed successfully")
        return True
    except Exception as e:
        print("❌ Failed to install packages: {}".format(e))
        return False

def setup_database():
    """Run database migrations"""
    print("\n💾 Setting up database...")
    try:
        python_path = get_venv_python()
        subprocess.check_call([python_path, 'manage.py', 'makemigrations'])
        subprocess.check_call([python_path, 'manage.py', 'migrate'])
        print("✅ Database setup completed")
        return True
    except Exception as e:
        print("❌ Database setup failed: {}".format(e))
        return False

def collect_static_files():
    """Collect static files"""
    print("\n📂 Collecting static files...")
    try:
        python_path = get_venv_python()
        subprocess.check_call([python_path, 'manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected")
        return True
    except Exception as e:
        print("❌ Failed to collect static files: {}".format(e))
        return False

def create_helper_scripts():
    """Create helper scripts for running the server and creating superuser"""
    print("\n📝 Creating helper scripts...")
    
    # Create run_server script for Windows
    if platform.system() == "Windows":
        with open('run_server.bat', 'w') as f:
            f.write('@echo off\n')
            f.write('echo 🚀 Starting GiftNest Server...\n')
            f.write('echo.\n')
            f.write('echo Server will be available at: http://127.0.0.1:8000/\n')
            f.write('echo Admin panel: http://127.0.0.1:8000/admin/\n')
            f.write('echo.\n')
            f.write('echo Press Ctrl+C to stop the server\n')
            f.write('echo.\n')
            f.write('venv\\Scripts\\python manage.py runserver\n')
            f.write('pause\n')
        
        with open('create_superuser.bat', 'w') as f:
            f.write('@echo off\n')
            f.write('echo 👤 Creating Superuser Account...\n')
            f.write('echo.\n')
            f.write('venv\\Scripts\\python manage.py createsuperuser\n')
            f.write('pause\n')
    else:
        # Create run_server script for Linux/Mac
        with open('run_server.sh', 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('echo "🚀 Starting GiftNest Server..."\n')
            f.write('echo ""\n')
            f.write('echo "Server will be available at: http://127.0.0.1:8000/"\n')
            f.write('echo "Admin panel: http://127.0.0.1:8000/admin/"\n')
            f.write('echo ""\n')
            f.write('echo "Press Ctrl+C to stop the server"\n')
            f.write('echo ""\n')
            f.write('venv/bin/python manage.py runserver\n')
            f.write('read -p "Press enter to continue..."\n')
        
        # Make it executable
        os.chmod('run_server.sh', 0o755)
        
        # Create create_superuser script for Linux/Mac
        with open('create_superuser.sh', 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('echo "👤 Creating Superuser Account..."\n')
            f.write('echo ""\n')
            f.write('venv/bin/python manage.py createsuperuser\n')
            f.write('read -p "Press enter to continue..."\n')
        
        # Make it executable
        os.chmod('create_superuser.sh', 0o755)
    
    print("✅ Helper scripts created")

def setup_environment_file():
    """Create .env file from .env.example if it doesn't exist"""
    print("\n⚙️  Setting up environment configuration...")
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ Environment file created from example")
        else:
            # Create a basic .env file
            with open('.env', 'w') as f:
                f.write("# Django Settings\n")
                f.write("SECRET_KEY=django-insecure-hgfokp*%5z5l$kem4#iwhs3%)rt&qf)1007zmoo7g7x!t+izhl\n")
                f.write("DEBUG=True\n")
                f.write("ALLOWED_HOSTS=localhost,127.0.0.1\n\n")
                f.write("# Razorpay Payment Gateway Settings\n")
                f.write("RAZORPAY_KEY_ID=rzp_test_your_key_id\n")
                f.write("RAZORPAY_KEY_SECRET=your_razorpay_secret_key\n")
                f.write("RAZORPAY_ENABLED=True\n\n")
                f.write("# Payment Gateway Settings\n")
                f.write("DEFAULT_PAYMENT_GATEWAY=razorpay\n")
                f.write("DEFAULT_CURRENCY=INR\n")
            print("✅ Basic environment file created")
    else:
        print("✅ Environment file already exists")

def main():
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if we're already in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  You are currently in a virtual environment!")
        print("Please deactivate it first and run this script again.")
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Setup environment file
    setup_environment_file()
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    # Collect static files
    collect_static_files()  # Not critical for basic operation
    
    # Create helper scripts
    create_helper_scripts()
    
    print("\n" + "=" * 60)
    print("🎉 Setup Completed Successfully!")
    print("=" * 60)
    print("\n🚀 To start the server:")
    if platform.system() == "Windows":
        print("   Double-click 'run_server.bat' OR")
        print("   Run: venv\\Scripts\\python manage.py runserver")
    else:
        print("   Run: ./run_server.sh OR")
        print("   Run: venv/bin/python manage.py runserver")
    
    print("\n👤 To create an admin user:")
    if platform.system() == "Windows":
        print("   Double-click 'create_superuser.bat' OR")
        print("   Run: venv\\Scripts\\python manage.py createsuperuser")
    else:
        print("   Run: ./create_superuser.sh OR")
        print("   Run: venv/bin/python manage.py createsuperuser")
    
    print("\n🌐 Access your site at: http://127.0.0.1:8000/")
    print("   Admin panel at: http://127.0.0.1:8000/admin/")
    
    print("\n📝 Next steps:")
    print("   1. Create a superuser account")
    print("   2. Start the development server")
    print("   3. Visit http://127.0.0.1:8000/ in your browser")
    print("   4. Login to admin panel and configure products")
    
    print("\n💳 Payment Gateway:")
    print("   Razorpay is configured in test mode by default")
    print("   For production, update .env with your live credentials")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()