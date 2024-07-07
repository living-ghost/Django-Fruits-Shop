from django.urls import path, include
from . import views


urlpatterns = [

    # User Section

    path('', views.user_login_view, name='user_login_view'),
    path('user/register/', views.user_register_view, name='user_register_view'),
    path('user/logout/', views.user_logout_view, name='user_logout_view'),

    # Others Section

    path('user/index/', views.user_index_view, name='user_index_view'),
    path('user/product/', views.user_product_view, name='user_product_view'),
    path('user/about/', views.user_about_view, name='user_about_view'),
    path('user/blog/', views.user_blog_view, name='user_blog_view'),
    path('user/contact/', views.user_contact_view, name='user_contact_view'),
    path('user/feature/', views.user_feature_view, name='user_feature_view'),
    path('user/testimonial/', views.user_testimonial_view, name='user_testimonial_view'),

    # User Profile Section

    path('user/profile/', views.user_profile_view, name='user_profile_view'),
    path('user/profile/edit/<int:user_id>/', views.user_edit_profile, name='user_edit_profile'),
    path('user/profile/delete/<int:user_id>/', views.user_delete_profile, name='user_delete_profile'),
    path('user/profile/change/password/<int:user_id>', views.user_chpwd_profile, name='user_chpwd_profile'),

    # User Checkout Section

    path('product/cart/', views.user_cart_view, name='user_cart_view'),
    path('product/cart/add/<int:product_id>/', views.user_add_cart_item_view, name='user_add_cart_item_view'),
    path('product/cart/update/<int:item_id>/', views.user_update_cart_item_view, name='user_update_cart_item_view'),
    path('product/cart/remove/<int:item_id>/', views.user_remove_cart_item_view, name='user_remove_cart_item_view'),
    path('cart/checkout/', views.user_checkout_view, name='user_checkout_view'),

    # Error Page Section

    path('error/', views.error_view, name='error_view'),

    # Admin Section

    path('administrator/login/', views.admin_login_view, name='admin_login_view'),
    path('administrator/register/', views.admin_register_view, name='admin_register_view'),
    path('administrator/logut/', views.admin_logout_view, name='admin_logout_view'),
    path('administrator/index/', views.admin_index_view, name='admin_index_view'),

    # Admin Product Section

    path('administrator/add/product/', views.admin_add_product, name='admin_add_product'),
    path('administrator/delete/product/<int:product_id>/', views.admin_delete_product, name='admin_delete_product'),
    path('administrator/update/product/<int:product_id>/', views.admin_update_product, name='admin_update_product'),

    # Admin Profile Section
    
    path('administrator/profile/', views.admin_profile, name='admin_profile'),
    path('administrator/profile/edit/<int:admin_id>/', views.admin_edit_profile, name='admin_edit_profile'),
    path('administrator/profile/delete/<int:admin_id>/', views.admin_delete_profile, name='admin_delete_profile'),
    path('administrator/profile/change/password/<int:admin_id>', views.admin_chpwd_profile, name='admin_chpwd_profile'),

    # Include Django's built-in authentication views
    path('accounts/', include('django.contrib.auth.urls')),

]