from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from orders.models import Order, OrderItem
from decimal import Decimal

class OrderViewsTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test products
        self.product1 = Product.objects.create(
            name='Test Product 1',
            slug='test-product-1',
            description='Test product description 1',
            price=Decimal('100.00'),
            stock=10,
            available=True
        )
        
        self.product2 = Product.objects.create(
            name='Test Product 2',
            slug='test-product-2',
            description='Test product description 2',
            price=Decimal('200.00'),
            stock=5,
            available=True
        )
        
    def test_order_create_view_unauthenticated(self):
        """Test order creation view when not authenticated"""
        response = self.client.get(reverse('orders:order_create'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        
    def test_order_create_view_authenticated_empty_cart(self):
        """Test order creation view when authenticated but cart is empty"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('orders:order_create'))
        # Should redirect to product list
        self.assertEqual(response.status_code, 302)
        
    def test_order_create_view_authenticated_with_items(self):
        """Test order creation view when authenticated with items in cart"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Add items to cart
        self.client.post(
            reverse('cart:cart_add', args=[self.product1.id]),
            {'quantity': 2}
        )
        
        # Try to create order
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/create.html')
        
    def test_order_detail_view(self):
        """Test order detail view"""
        # Login user
        self.client.login(username='testuser', password='testpass123')
        
        # Create an order
        order = Order.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address='123 Test St',
            postal_code='12345',
            city='Test City'
        )
        
        # Create order item
        OrderItem.objects.create(
            order=order,
            product=self.product1,
            price=self.product1.price,
            quantity=2
        )
        
        response = self.client.get(
            reverse('orders:order_detail', args=[order.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/detail.html')
        self.assertContains(response, 'Test Product 1')
        
    def tearDown(self):
        """Clean up test data"""
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()