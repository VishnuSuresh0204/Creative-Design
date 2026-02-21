"""
URL configuration for creative project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_django/', admin.site.urls),
    
    # Auth
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('user_reg/', views.user_reg, name='user_reg'),
    path('seller_reg/', views.seller_reg, name='seller_reg'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin
    path('admin_home/', views.admin_home, name='admin_home'),
    path('manage_sellers/', views.manage_sellers, name='manage_sellers'),
    path('admin_view_users/', views.admin_view_users, name='admin_view_users'),
    path('admin_view_payments/', views.admin_view_payments, name='admin_view_payments'),
    
    # Seller
    path('seller_home/', views.seller_home, name='seller_home'),
    path('add_design/', views.add_design, name='add_design'),
    path('manage_design/', views.manage_design, name='manage_design'),
    path('edit_design/', views.edit_design, name='edit_design'),
    path('delete_design/', views.delete_design, name='delete_design'),
    path('seller_view_bookings/', views.seller_view_bookings, name='seller_view_bookings'),
    path('manage_booking_status/', views.manage_booking_status, name='manage_booking_status'),
    
    # User
    path('user_home/', views.user_home, name='user_home'),
    path('browse_designs/', views.browse_designs, name='browse_designs'),
    path('design_details/', views.design_details, name='design_details'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('user_make_payment/', views.user_make_payment, name='user_make_payment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
