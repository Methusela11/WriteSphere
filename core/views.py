from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from .models import Profile

# Create your views here.
def home(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Check passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        # Check username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "signup.html")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Save phone number if using custom model or profile (optional)
        # e.g., user.profile.phone = phone; user.profile.save()

        # Log the user in using Django's login
        login(request, user)  # this is safe now

        messages.success(request, f"Account created for {user.username}!")
        return redirect("login")

    return render(request, "signup.html")

def user_login(request):  # <-- rename this
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # <-- now calls Django's login correctly
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("dashboard")  # redirect to dashboard
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")





