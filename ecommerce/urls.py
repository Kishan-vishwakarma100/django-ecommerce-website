# Project-level urls.py
from django.contrib import admin
from django.urls import path, include
from products.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', home, name='home'),

    # Products app
    path('products/', include('products.urls')),  # <-- add 'products/' prefix

    # Accounts app
    path('accounts/', include('accounts.urls')),

    # Cart app
    path('cart/', include('cart.urls')),

    # Orders app
    path('orders/', include('orders.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)