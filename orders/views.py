from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponse
from django.template.loader import render_to_string

from cart.models import Cart, CartItem
from django.utils import timezone
from decimal import Decimal


# =========================
# ORDER LIST
# =========================
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_list.html', {'orders': orders})


# =========================
# ORDER DETAIL
# =========================
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Calculate item total dynamically
    for item in order.orderitem_set.all():
        item.item_total = item.product.price * item.quantity

    return render(request, 'order_detail.html', {'order': order})


# =========================
# CHECKOUT PAGE
# =========================
@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty!")
        return redirect('product_list')

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('product_list')

    # Calculate totals
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity

    total_price = sum(item.subtotal for item in cart_items)
    shipping_cost = Decimal('50.00') if total_price < Decimal('1000.00') else Decimal('0.00')
    tax_rate = Decimal('0.05')
    tax_amount = (total_price + shipping_cost) * tax_rate
    grand_total = total_price + shipping_cost + tax_amount

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'tax_amount': tax_amount,
        'grand_total': grand_total,
    }

    return render(request, 'checkout.html', context)


# =========================
# PLACE ORDER
# =========================
@login_required
def place_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty!")
        return redirect('product_list')

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('product_list')

    # Calculate totals
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    shipping_cost = Decimal('50.00') if total_price < Decimal('1000.00') else Decimal('0.00')
    tax_rate = Decimal('0.05')
    tax_amount = (total_price + shipping_cost) * tax_rate
    grand_total = total_price + shipping_cost + tax_amount

    # Create order
    order = Order.objects.create(
        user=request.user,
        total_price=grand_total,
        status='pending',
        created_at=timezone.now()
    )

    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    # Clear cart
    cart.items.all().delete()

    messages.success(request, f"Order #{order.id} placed successfully!")
    return render(request, 'order_success.html', {'order': order})


# =========================
# DOWNLOAD INVOICE (NO WEASYPRINT)
# =========================
@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Calculate item totals
    for item in order.orderitem_set.all():
        item.item_total = item.product.price * item.quantity

    html_string = render_to_string('invoice.html', {'order': order})

    response = HttpResponse(html_string, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.html"'

    return response


# =========================
# CANCEL ORDER
# =========================
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status in ['pending', 'processing']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, f"Order #{order.id} has been cancelled.")
    else:
        messages.warning(request, "This order cannot be cancelled.")

    return redirect('order_detail', order_id=order.id)