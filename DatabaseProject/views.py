from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.db import models
from .models import Users, Books


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


class AddBookForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    author = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    summary = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional'
        })
    )
    genre = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional'
        })
    )
    publish_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
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
            # user = Users(
            #     username=username,
            #     password=password,
            #     first_name=first_name,
            #     last_name=last_name,
            #     phone_number=phone_number,
            #     user_role='registered',
            #     outstanding_balance=0.00
            # )
            # user.save()

            Users.objects.raw("INSERT INTO Users(username, password, first_name, last_name, phone_number, user_role, outstanding_balance) VALUES (%s, %s, %s, %s, %s, 'registered', 0.00)", [username, password, first_name, last_name, phone_number])

            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def add_book_view(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            summary = form.cleaned_data['summary']
            genre = form.cleaned_data['genre']
            publish_year = form.cleaned_data['publish_year']

            if Books.objects.filter(title=title).exists():
                messages.error(request, 'The book is already in the library.')
                return render(request, 'add_book.html', {'form': form})

            # book = Books(
            #     title=title,
            #     author=author,
            #     summary=summary,
            #     genre=genre,
            #     publish_year=publish_year
            # )
            # book.save()
            
            Books.objects.raw("INSERT INTO Books(title, author, summary, genre, publish_year) VALUES (%s, %s, %s, %s, %s)", [title, author, summary, genre, publish_year])


            messages.success(request, 'Book added successfully.')
            return redirect('add_book')
    else:
        form = AddBookForm()

    return render(request, 'add_book.html', {'form': form})


def dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = Users.objects.get(user_id=request.session['user_id'])
    return render(request, 'dashboard.html', {'user': user})


def logout_view(request):
    request.session.flush()
    return redirect('login')


def search_books(request):
    query = request.GET.get('query', '')
    show_all = request.GET.get('show_all')
    books = []

    if show_all:
        # books = Books.objects.all().order_by('title')
        books = Books.objects.raw("SELECT * FROM Books ORDER BY title")
    elif query:
        # books = Books.objects.filter(
        #     models.Q(title__icontains=query) | models.Q(author__icontains=query)
        # )
        books = Books.objects.raw("SELECT * FROM Books WHERE title LIKE %%%s%% OR author LIKE %%%s%%", [query, query])
    return render(request, 'search.html', {'books': books, 'query': query})
