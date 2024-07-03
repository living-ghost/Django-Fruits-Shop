from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User, Admin, Products

# Create your views here.



# User Section

@login_required
def user_index_view(request):
    return render(request, "user_index.html")


def user_register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'user_login.html')
        if User.objects.filter(email=email).exists():
            return render(request, 'user_login.html')
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect('user_login_view')
    else:
        return render(request, 'user_register.html')


def user_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and isinstance(user, User):
            login(request, user)
            return redirect('user_index_view')
        else:
            return render(request, 'user_login.html')
    return render(request, 'user_login.html')


@login_required
def user_logout_view(request):
    logout(request)
    return redirect('user_login_view')



# Admin Section

@login_required
def admin_index_view(request):

    products = Products.objects.all()

    return render(request, "admin_index.html", {'products' : products})


def admin_register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if Admin.objects.filter(username=username).exists():
            return render(request, 'admin_login.html')
        if Admin.objects.filter(email=email).exists():
            return render(request, 'admin_login.html')
        admin = Admin.objects.create_admin(username=username, email=email, password=password)
        return redirect('admin_login_view')
    else:
        return render(request, 'admin_register.html')


def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = authenticate(request, username=username, password=password)
        if admin is not None and isinstance(admin, Admin):
            login(request, admin)
            return redirect('admin_index_view')
        else:
            error = "invalid credentials"
            return render(request, 'admin_login.html', {'error': error})
    return render(request, 'admin_login.html')


@login_required
def admin_logout_view(request):
    logout(request)
    return redirect('admin_login_view')



# Product Adding/Deleting/Editing Section

@login_required
def admin_add_product(request):
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



# Other Sections

def user_product_view(request):
    return render(request, "user_product.html")


def user_about_view(request):
    return render(request, "user_about.html")


def user_blog_view(request):
    return render(request, "user_blog.html")


def user_contact_view(request):
    return render(request, "user_contact.html")


def user_feature_view(request):
    return render(request, "user_feature.html")


def user_testimonial_view(request):
    return render(request, "user_testimonial.html")


def error_view(request):
    return render(request, "404.html")