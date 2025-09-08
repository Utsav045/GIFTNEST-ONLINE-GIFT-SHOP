from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal

class CartViewsTest(TestCase):
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
        
    def test_cart_detail_view(self):
        """Test cart detail view"""
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        
    def test_add_to_cart(self):
        """Test adding product to cart"""
        # Add product to cart
        response = self.client.post(
            reverse('cart:cart_add', args=[self.product1.id]),
            {'quantity': 2},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        
        # Check if product is in cart
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response, 'Test Product 1')
        
    def test_remove_from_cart(self):
        """Test removing product from cart"""
        # First add product to cart
        self.client.post(
            reverse('cart:cart_add', args=[self.product1.id]),
            {'quantity': 1}
        )
        
        # Then remove it
        response = self.client.post(
            reverse('cart:cart_remove', args=[self.product1.id]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        
        # Check that product is no longer in cart
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertNotContains(response, 'Test Product 1')
        
    def test_cart_update(self):
        """Test updating cart quantities"""
        # Add product to cart
        self.client.post(
            reverse('cart:cart_add', args=[self.product1.id]),
            {'quantity': 1}
        )
        
        # Update quantity
        response = self.client.post(
            reverse('cart:cart_update', args=[self.product1.id]),
            {'quantity': 3},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        
    def tearDown(self):
        """Clean up test data"""
        Product.objects.all().delete()
        User.objects.all().delete()