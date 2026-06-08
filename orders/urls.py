from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('download-invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),

]