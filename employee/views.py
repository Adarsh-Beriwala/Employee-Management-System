from django.shortcuts import render, redirect
from .models import Employee

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# 🧾 EMPLOYEE SIGNUP
def employee_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 👉 check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'employee_signup.html', {'error': 'Username already exists'})

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/login/')

    return render(request, 'employee_signup.html')


# 🔐 EMPLOYEE LOGIN
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# 👑 ADMIN LOGIN
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        # 👉 only admin allowed
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid admin credentials'})

    return render(request, 'admin_login.html')


# 🔒 HOME (RBAC + FILTER)
@login_required
def home(request):

    # 👉 ONLY ADMIN CAN ADD
    if request.method == 'POST' and request.user.is_staff:
        name = request.POST.get('name')
        department = request.POST.get('department')
        role = request.POST.get('role')

        Employee.objects.create(
            name=name,
            department=department,
            role=role
        )

    # 🔍 FILTERING
    name = request.GET.get('name')
    department = request.GET.get('department')
    role = request.GET.get('role')

    employees = Employee.objects.all()

    if name:
        employees = employees.filter(name__icontains=name)

    if department:
        employees = employees.filter(department__icontains=department)

    if role:
        employees = employees.filter(role__icontains=role)

    return render(request, 'home.html', {'employees': employees})


# 🗑 DELETE (ADMIN ONLY)
@login_required
def delete_employee(request, id):
    if not request.user.is_staff:
        return redirect('/')

    try:
        emp = Employee.objects.get(id=id)
        emp.delete()
    except Employee.DoesNotExist:
        pass

    return redirect('/')


# 🚪 LOGOUT
def logout_user(request):
    logout(request)
    return redirect('/login/')