from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required


def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_user_cart(request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_detail')


@login_required
def remove_from_cart(request, product_id):
    cart = get_user_cart(request.user)

    cart_item = CartItem.objects.filter(
        cart=cart,
        product_id=product_id
    ).first()

    # Avoid 404 crash if item doesn't exist
    if cart_item:
        cart_item.delete()

    return redirect('cart:cart_detail')


@login_required
def update_cart_item(request, product_id):
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1

        cart = get_user_cart(request.user)

        cart_item = CartItem.objects.filter(
            cart=cart,
            product_id=product_id
        ).first()

        # If item doesn't exist, just redirect safely
        if not cart_item:
            return redirect('cart:cart_detail')

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart:cart_detail')


@login_required
def cart_detail(request):
    cart = get_user_cart(request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    return render(request, 'cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items
    })

