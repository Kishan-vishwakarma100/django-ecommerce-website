from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.db.models import Q
from .forms import RegisterForm

User = get_user_model()


# -------- REGISTER VIEW --------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'register.html', {'form': form})


# -------- LOGIN VIEW --------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Single optimized query (username OR email)
        user_obj = User.objects.filter(
            Q(username=username_or_email) |
            Q(email__iexact=username_or_email)
        ).first()

        if user_obj:
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
        else:
            user = None

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username/email or password")

    return render(request, 'login.html')


# -------- LOGOUT VIEW --------
def logout_view(request):
    logout(request)
    return redirect('login')