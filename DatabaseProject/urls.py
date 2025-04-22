"""
URL configuration for DatabaseProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Login page as the main page
    path('register/', views.register_view, name='register'),  # Registration page
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard after login
    path('logout/', views.logout_view, name='logout'),  # Logout functionality
    path('admin/', admin.site.urls),
    path('search/', views.search_books, name='search_books'), # search for books page
    path('add_book/', views.add_book_view, name='add_book'),
    path('place_hold/', views.place_hold, name='place_hold'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('reserve_book/', views.reserve_book, name='reserve_book'),
    path('return_book/', views.return_book, name='return_book'),
    path('cancel_hold/', views.cancel_hold, name='cancel_hold'),
    path('admin_delete_hold/', views.admin_delete_hold, name='admin_delete_hold'),
    path('admin_end_reservation/', views.admin_end_reservation, name='admin_end_reservation'),
    path('clear_balance/', views.clear_balance, name='clear_balance'),
    path('pay_balance/', views.pay_balance, name='pay_balance'),
    path('add_copy/', views.add_copy, name='add_copy')
]