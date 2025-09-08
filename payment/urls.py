from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    # Main payment processing
    path('process/<int:order_id>/', views.payment_process, name='process'),
    path('success/<int:order_id>/', views.payment_success, name='success'),
    path('cancel/<int:order_id>/', views.payment_cancel, name='cancel'),
    
    # Webhooks
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('webhook/razorpay/', views.razorpay_webhook, name='razorpay_webhook'),
    
    # Payment verification
    path('verify/razorpay/', views.razorpay_verify_payment, name='razorpay_verify'),
]
