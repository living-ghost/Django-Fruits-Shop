from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotAllowed
from .models import User, Admin, Products, Cart, CartItem


# User Section

@login_required
def user_index_view(request):
    """
    Renders the user index view.
    """
    return render(request, "user_index.html")


def user_register_view(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'user_login.html')
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('user_login_view')
    return render(request, 'user_register.html')


def user_login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and isinstance(user, User):
            login(request, user)
            return redirect('user_index_view')
        return render(request, 'user_login.html')
    return render(request, 'user_login.html')


@login_required
def user_logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    return redirect('user_login_view')


# User Profile Section

@login_required
def user_profile_view(request):
    """
    Renders the user profile view.
    """
    return render(request, "user_profile.html")


@login_required
def user_edit_profile(request, user_id):
    """
    Handles user profile editing.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username and email:
            user.username = username
            user.email = email
            user.save()
    return render(request, "user_edit_profile.html", {'user': user})


@login_required
def user_delete_profile(request, user_id):
    """
    Handles user profile deletion.
    """
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('user_register_view')
    return HttpResponseNotAllowed(['POST'])


@login_required
def user_chpwd_profile(request, user_id):
    """
    Handles user password change.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        current_password = request.POST.get('Current_Password')
        new_password = request.POST.get('New_Password')
        re_new_password = request.POST.get('Re_New_Password')
        if user.check_password(current_password):
            if new_password == re_new_password:
                user.set_password(new_password)
                user.save()
            else:
                print("Passwords Not Matching")
        else:
            print("Current password is wrong")
    return render(request, 'user_chpwd_profile.html', {'user': user})


# Admin Section

@login_required
def admin_index_view(request):
    """
    Renders the admin index view with all products.
    """
    products = Products.objects.all()
    return render(request, "admin_index.html", {'products': products})


def admin_register_view(request):
    """
    Handles admin registration.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if Admin.objects.filter(username=username).exists() or Admin.objects.filter(email=email).exists():
            return render(request, 'admin_login.html')
        Admin.objects.create_admin(username=username, email=email, password=password)
        return redirect('admin_login_view')
    return render(request, 'admin_register.html')


def admin_login_view(request):
    """
    Handles admin login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = authenticate(request, username=username, password=password)
        if admin is not None and isinstance(admin, Admin):
            login(request, admin)
            return redirect('admin_index_view')
        error = "Invalid credentials"
        return render(request, 'admin_login.html', {'error': error})
    return render(request, 'admin_login.html')


@login_required
def admin_logout_view(request):
    """
    Handles admin logout.
    """
    logout(request)
    return redirect('admin_login_view')


# Admin Product Section

@login_required
def admin_add_product(request):
    """
    Handles adding a new product.
    """
    if request.method == 'POST':
        product_image = request.FILES.get('image')
        product_name = request.POST.get('name')
        product_off_price = request.POST.get('offer_price')
        product_old_price = request.POST.get('old_price')
        product_category = request.POST.get('category')
        
        if product_image and product_name and product_off_price and product_old_price and product_category:
            product = Products(
                product_image=product_image,
                product_name=product_name,
                product_off_price=product_off_price,
                product_old_price=product_old_price,
                product_category=product_category
            )
            product.save()
            return redirect('admin_index_view')
    return render(request, 'admin_index.html')


@login_required
def admin_delete_product(request, product_id):
    """
    Handles deleting a product.
    """
    if request.method == 'POST':
        product = get_object_or_404(Products, id=product_id)
        product.delete()
        return redirect("admin_index_view")
    return HttpResponseNotAllowed(['POST'])


@login_required
def admin_update_product(request, product_id):
    """
    Handles updating a product.
    """
    product = get_object_or_404(Products, id=product_id)
    if request.method == 'POST':
        product_image = request.FILES.get('image')
        product_name = request.POST.get('name')
        product_off_price = request.POST.get('offer_price')
        product_old_price = request.POST.get('old_price')
        product_category = request.POST.get('category')
        
        if product_name and product_category:
            if product_image:
                product.product_image = product_image
            product.product_name = product_name
            product.product_off_price = product_off_price
            product.product_old_price = product_old_price
            product.product_category = product_category
            product.save()
            return redirect('admin_index_view')
    return render(request, 'admin_index.html')


# Admin Profile Section

@login_required
def admin_profile(request):
    """
    Renders the admin profile view.
    """
    admin = get_object_or_404(Admin, id=request.user.id)
    return render(request, "admin_profile.html", {'admin': admin})


@login_required
def admin_edit_profile(request, admin_id):
    """
    Handles editing the admin profile.
    """
    admin = get_object_or_404(Admin, id=admin_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username and email:
            admin.username = username
            admin.email = email
            admin.save()
    return render(request, "admin_edit_profile.html", {'admin': admin})


@login_required
def admin_delete_profile(request, admin_id):
    """
    Handles deleting the admin profile.
    """
    if request.method == 'POST':
        admin = get_object_or_404(Admin, id=admin_id)
        admin.delete()
        return redirect('admin_register_view')
    return HttpResponseNotAllowed(['POST'])


@login_required
def admin_chpwd_profile(request, admin_id):
    """
    Handles admin password change.
    """
    admin = get_object_or_404(Admin, id=admin_id)
    if request.method == 'POST':
        current_password = request.POST.get('Current_Password')
        new_password = request.POST.get('New_Password')
        re_new_password = request.POST.get('Re_New_Password')
        if admin.check_password(current_password):
            if new_password == re_new_password:
                admin.set_password(new_password)
                admin.save()
            else:
                print("Passwords Not Matching")
        else:
            print("Current password is wrong")
    return render(request, 'admin_chpwd_profile.html', {'admin': admin})


# Other Sections

def user_product_view(request):
    """
    Renders the user product view.
    """
    products = Products.objects.all()
    return render(request, "user_product.html", {'products': products})


def user_about_view(request):
    """
    Renders the user about view.
    """
    return render(request, "user_about.html")


def user_blog_view(request):
    """
    Renders the user blog view.
    """
    return render(request, "user_blog.html")


def user_contact_view(request):
    """
    Renders the user contact view.
    """
    return render(request, "user_contact.html")


def user_feature_view(request):
    """
    Renders the user feature view.
    """
    return render(request, "user_feature.html")


def user_testimonial_view(request):
    """
    Renders the user testimonial view.
    """
    return render(request, "user_testimonial.html")


def error_view(request):
    """
    Renders the error view.
    """
    return render(request, "404.html")


# Adding to Cart & Checkout Section

def user_cart_view(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    grand_total = cart.grand_total
    return render(request, "user_cart.html", {'cart' : cart, 'grand_total' : grand_total})


def user_add_cart_item_view(request, product_id):
    user = request.user
    product = get_object_or_404(Products, id=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('user_cart_view')


def user_update_cart_item_view(request, item_id):
    if request.method == 'POST':
        item = CartItem.objects.get(id=item_id)
        action = request.POST.get('action')
        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease' and item.quantity > 1:
            item.quantity -= 1
        item.save()
    return redirect('user_cart_view')


def user_remove_cart_item_view(request, item_id):
    if request.method == 'POST':
        item = CartItem.objects.get(id=item_id)
        item.delete()
    return redirect('user_cart_view')


def user_checkout_view(request):
    return render(request, "user_checkout.html")