from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),

    # 👤 Employee
    path('signup/', views.employee_signup),
    path('login/', views.login_user),

    # 👑 Admin
    path('admin-login/', views.admin_login),

    # 🔐 Auth
    path('logout/', views.logout_user),

    # 🗑 Delete
    path('delete/<int:id>/', views.delete_employee),
]