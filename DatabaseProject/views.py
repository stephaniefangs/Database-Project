from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .models import Users

# Define forms
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'login-username',
            'name': 'login-username',
            'autocomplete': 'off'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'login-password',
            'name': 'login-password',
            'autocomplete': 'off'
        })
    )

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional'
        })
    )
    last_name = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional'
        })
    )
    phone_number = forms.CharField(
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional'
        })
    )

# View functions
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                # Direct password comparison (need to change when password is hashed)
                user = Users.objects.get(username=username, password=password)
                # Store user info in session
                request.session['user_id'] = user.user_id
                request.session['username'] = user.username
                request.session['user_role'] = user.user_role
                return redirect('dashboard')
            except Users.DoesNotExist:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            
            # Check if passwords match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return render(request, 'register.html', {'form': form})
            
            # Check if username already exists
            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'register.html', {'form': form})
            
            # Create new user
            user = Users(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                user_role='registered',
                outstanding_balance=0.00
            )
            user.save()
            
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user = Users.objects.get(user_id=request.session['user_id'])
    return render(request, 'dashboard.html', {'user': user})

def logout_view(request):
    request.session.flush()
    return redirect('login')