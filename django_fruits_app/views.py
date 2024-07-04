from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotAllowed
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



@login_required
def admin_delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, id=product_id)
        product.delete()
        return redirect("admin_index_view")
    return render(request,"admin_index_view")



@login_required
def admin_update_product(request, product_id):
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

def admin_profile(request):
    admin = get_object_or_404(Admin, id=request.user.id)
    return render(request, "admin_profile.html", {'admin' : admin})


@login_required
def admin_edit_profile(request, admin_id):
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
    if request.method == 'POST':
        admin = get_object_or_404(Admin, id=admin_id)
        admin.delete()

        return redirect('admin_register_view')
    else:
        return HttpResponseNotAllowed(['POST'])
        
@login_required
def admin_chpwd_profile(request, admin_id):
    admin = get_object_or_404(Admin, id=admin_id)
    if request.method == 'POST':
        Current_Password = request.POST.get('Current_Password')
        New_Password = request.POST.get('New_Password')
        Re_New_Password = request.POST.get('Re_New_Password')
        if admin.check_password(Current_Password):
            if New_Password == Re_New_Password:
                admin.set_password(New_Password)
                admin.save()
            else:
                print("Passwords Not Matching")
        else:
            print("Current password is wrong")

    return render(request, 'admin_chpwd_profile.html', {'admin' : admin})
        


# User Profile Section

def user_profile_view(request):
    return render(request, "user_profile.html")


@login_required
def user_edit_profile(request, user_id):
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
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()

        return redirect('user_register_view')
    else:
        return HttpResponseNotAllowed(['POST'])
        
@login_required
def user_chpwd_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        Current_Password = request.POST.get('Current_Password')
        New_Password = request.POST.get('New_Password')
        Re_New_Password = request.POST.get('Re_New_Password')
        if user.check_password(Current_Password):
            if New_Password == Re_New_Password:
                user.set_password(New_Password)
                user.save()
            else:
                print("Passwords Not Matching")
        else:
            print("Current password is wrong")

    return render(request, 'user_chpwd_profile.html', {'user' : user})


# Other Sections

def user_product_view(request):
    products = Products.objects.all()
    return render(request, "user_product.html", {'products' : products})


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