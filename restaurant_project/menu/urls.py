from django.urls import path
from . import views
from .views import CustomLoginView
from .views import order_history_view



urlpatterns = [
    path('', views.index_view, name='home'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:dish_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:dish_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('update-cart-all/', views.update_cart_all, name='update_cart_all'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'),
    path('order-history/', order_history_view, name='order_history'),
]
