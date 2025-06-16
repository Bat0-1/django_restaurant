from datetime import datetime
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Category
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from .forms import EmailLoginForm
from .models import Order
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .models import Dish




# Common headers for API
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# Home Page View: Display and filter dishes
def index_view(request):
    category_id = request.GET.get('category')
    is_vegetarian = request.GET.get('vegetarian') == 'true'
    contains_nuts = request.GET.get('nuts') == 'true'
    spiciness = request.GET.get('spice')

    dishes = Dish.objects.all()

    if category_id:
        dishes = dishes.filter(category__id=category_id)

    if is_vegetarian:
        dishes = dishes.filter(vegetarian=True)

    if contains_nuts:
        dishes = dishes.filter(nuts=True)

    if spiciness not in [None, "", "-1"]:
        try:
            spice_level = int(spiciness)
            dishes = dishes.filter(spiciness=spice_level)
        except ValueError:
            pass

    categories = Category.objects.all()

    return render(request, 'menu/index.html', {
        'dishes': dishes,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'filters': {
            'vegetarian': is_vegetarian,
            'nuts': contains_nuts,
            'spice': spiciness,
        },
        'current_year': datetime.now().year
    })




# Cart View: Display cart contents
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    # Fetch all dishes from your own database
    all_dishes = Dish.objects.all()

    for dish in all_dishes:
        dish_id_str = str(dish.id)
        if dish_id_str in cart:
            quantity = cart[dish_id_str]
            subtotal = dish.price * quantity
            cart_items.append({
                'id': dish.id,
                'name': dish.name,
                'price': dish.price,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal

    return render(request, 'menu/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# Add to Cart
def add_to_cart(request, dish_id):
    cart = request.session.get('cart', {})
    cart[str(dish_id)] = cart.get(str(dish_id), 0) + 1
    request.session['cart'] = cart
    return redirect('home')

# Update Single Cart Item (+ or - or custom number)
def update_cart(request, dish_id, action):
    cart = request.session.get('cart', {})
    str_id = str(dish_id)

    if action == 'add':
        cart[str_id] = cart.get(str_id, 0) + 1
    elif action == 'remove':
        if str_id in cart:
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]
    elif action.isdigit():
        cart[str_id] = max(1, int(action))  # set to new value, min = 1

    request.session['cart'] = cart
    return redirect('cart')

# Remove an Item from Cart
def remove_from_cart(request, dish_id):
    cart = request.session.get('cart', {})
    cart.pop(str(dish_id), None)
    request.session['cart'] = cart
    return redirect('cart')

# Clear Entire Cart
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart')

# updating cart with manual input
@require_POST
def update_cart_all(request):
    cart = request.session.get('cart', {})
    for key, value in request.POST.items():
        if key.startswith("qty_"):
            try:
                product_id = key.split("_")[1]
                quantity = int(value)
                if quantity > 0:
                    cart[product_id] = quantity
                else:
                    cart.pop(product_id, None)
            except:
                continue

    request.session['cart'] = cart
    return redirect('cart')

# Order View: Place an order
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    # Fetch dishes and calculate total
    total = 0
    dishes = []
    for dish_id, quantity in cart.items():
        try:
            dish = Dish.objects.get(id=int(dish_id))
            total += dish.price * quantity
            dishes.append(dish)
        except Dish.DoesNotExist:
            pass

    form = CheckoutForm(request.POST or None)

    if request.method == 'POST' and request.user.is_authenticated and form.is_valid():
        last_order = Order.objects.filter(user=request.user).aggregate(Max('user_order_number'))
        next_num = (last_order['user_order_number__max'] or 0) + 1

        order = Order.objects.create(
            user=request.user,
            items=cart,
            address=form.cleaned_data['address'],
            phone=form.cleaned_data['phone'],
            notes=form.cleaned_data['notes'],
            total_price=total,
            user_order_number=next_num,
        )
        request.session['cart'] = {}  # Clear cart after ordering
        return redirect('order_success', order_id=order.id)

    return render(request, 'menu/checkout.html', {
        'form': form,
        'total': total,
        'require_login': not request.user.is_authenticated,  # <-- KEY LINE
    })



def order_success_view(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'menu/order_success.html', {'order': order})




# Signup and Login Views
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or wherever you'd like to redirect
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = EmailLoginForm


def logout_view(request):
    logout(request)
    return redirect('home')

# Order History View: Display user's order history
@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'menu/order_history.html', {
        'orders': orders,
        'current_year': datetime.now().year
    })