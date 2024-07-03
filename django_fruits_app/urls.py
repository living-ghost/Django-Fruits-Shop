from django.urls import path
from . import views


urlpatterns = [

    path('', views.user_login_view, name='user_login_view'),
    path('user_register/', views.user_register_view, name='user_register_view'),
    path('user_logout/', views.user_logout_view, name='user_logout_view'),
    path('user_index/', views.user_index_view, name='user_index_view'),
    path('user_product/', views.user_product_view, name='user_product_view'),
    path('user_about/', views.user_about_view, name='user_about_view'),
    path('user_blog/', views.user_blog_view, name='user_blog_view'),
    path('user_contact/', views.user_contact_view, name='user_contact_view'),
    path('user_feature/', views.user_feature_view, name='user_feature_view'),
    path('user_testimonial/', views.user_testimonial_view, name='user_testimonial_view'),
    path('error/', views.error_view, name='error_view'),

    path('admin_login/', views.admin_login_view, name='admin_login_view'),
    path('admin_register/', views.admin_register_view, name='admin_register_view'),
    path('admin_logut/', views.admin_logout_view, name='admin_logout_view'),
    path('admin_index/', views.admin_index_view, name='admin_index_view'),
    path('admin_add_product/', views.admin_add_product, name='admin_add_product'),
    
]