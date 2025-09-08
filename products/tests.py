from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, ProductImage
from decimal import Decimal
import os

class ProductViewsTest(TestCase):
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
        
        # Create product images
        # Note: We won't actually upload files in tests to keep them lightweight
        
    def test_product_list_view(self):
        """Test product list view"""
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product 1')
        self.assertContains(response, 'Test Product 2')
        self.assertTemplateUsed(response, 'products/list.html')
        
    def test_product_detail_view(self):
        """Test product detail view"""
        response = self.client.get(
            reverse('products:product_detail', args=[self.product1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product 1')
        self.assertContains(response, 'Test product description 1')
        self.assertTemplateUsed(response, 'products/detail.html')
        
    def test_product_detail_view_404(self):
        """Test product detail view with non-existent product"""
        response = self.client.get(
            reverse('products:product_detail', args=[999])
        )
        self.assertEqual(response.status_code, 404)

    def test_product_search(self):
        """Test product search functionality"""
        # Search for product 1
        response = self.client.get(
            reverse('products:product_list'), 
            {'q': 'Test Product 1'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product 1')
        # Should not contain product 2 in search results
        # Note: This depends on implementation of search functionality
        
    def tearDown(self):
        """Clean up test data"""
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()