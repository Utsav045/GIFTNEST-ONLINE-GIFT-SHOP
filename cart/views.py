from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from django.contrib import messages
from .cart import Cart
import logging

logger = logging.getLogger(__name__)

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {
        'cart': cart
    })

@require_POST
def cart_add(request, product_id):
    logger.info(f"Cart add called for product {product_id} by user {request.user}")
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    logger.info(f"Adding {quantity} of product {product.name} to cart")
    
    # Check if there's enough stock
    if quantity > product.stock:
        messages.error(request, f'Sorry, only {product.stock} items available.')
        logger.warning(f"Insufficient stock for product {product.name}: requested {quantity}, available {product.stock}")
        return redirect('products:product_detail', id=product_id)
    
    # Check if this is an update from cart page (has existing quantity) or new add
    product_id_str = str(product_id)
    is_update_from_cart = product_id_str in cart.cart
    
    if is_update_from_cart:
        # This is an update from cart page - replace the quantity
        cart.add(product=product, quantity=quantity, override_quantity=True)
        messages.success(request, f'{product.name} quantity updated to {quantity}.')
        logger.info(f"Updated {product.name} quantity to {quantity} in cart")
    else:
        # This is a new add from product page - add to existing quantity
        cart.add(product=product, quantity=quantity)
        messages.success(request, f'{product.name} added to cart.')
        logger.info(f"Successfully added {product.name} to cart")
    
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'{product.name} removed from cart.')
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, product_id):
    """Update quantity of a product already in cart"""
    logger.info(f"Cart update called for product {product_id} by user {request.user}")
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    logger.info(f"Updating {product.name} quantity to {quantity} in cart")
    
    # Check if there's enough stock
    if quantity > product.stock:
        messages.error(request, f'Sorry, only {product.stock} items available.')
        logger.warning(f"Insufficient stock for product {product.name}: requested {quantity}, available {product.stock}")
        return redirect('cart:cart_detail')
    
    # Update the quantity (replace existing)
    cart.add(product=product, quantity=quantity, override_quantity=True)
    messages.success(request, f'{product.name} quantity updated to {quantity}.')
    logger.info(f"Successfully updated {product.name} quantity to {quantity}")
    
    return redirect('cart:cart_detail')

def cart_debug(request):
    cart = Cart(request)
    return render(request, 'cart/debug.html', {
        'cart': cart
    })
