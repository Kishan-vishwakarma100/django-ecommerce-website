from django.urls import path
from . import views



urlpatterns = [
    path("", views.product_list, name="product_list"),  
    path("<slug:slug>/", views.product_detail, name="product_detail"), 
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),

]