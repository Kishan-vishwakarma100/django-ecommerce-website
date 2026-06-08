from django.shortcuts import render,redirect
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from django.contrib import messages


@login_required(login_url='login')
def home(request):
    products = Product.objects.all()
    return render(request,"home.html",{"products":products})


def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, "product_list.html", {"products": products})



def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    context = {
        "product": product,
        "related_products": related_products
    }

    return render(request,"product_detail.html",context)


@login_required(login_url='login')
def buy_now(request, product_id):
    """
    Adds a single product to the cart and redirects to checkout.
    If already in cart, increments quantity by 1.
    """

    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is out of stock!")
        return redirect('product_detail', slug=product.slug)

    # Get or create user's cart
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Get or create cart item
    cart_item, created_item = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created_item:
        # Increment quantity only if stock allows
        if cart_item.quantity + 1 > product.stock:
            messages.warning(request, f"Only {product.stock} units of {product.name} available.")
        else:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart successfully!")

    # Redirect to checkout page
    return redirect('checkout')