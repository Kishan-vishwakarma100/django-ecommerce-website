from django.db import models
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s Cart"

    # ✅ Total number of items
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    # ✅ Total cart price
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.select_related('product'))

    # ✅ Optional: for cleaner template usage
    @property
    def total_price(self):
        return self.get_total_price()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    # ✅ Subtotal per item
    def get_total_price(self):
        return self.product.price * self.quantity