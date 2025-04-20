from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.db import models, connection
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
                # user = Users.objects.get(username=username, password=password)
                user = Users.objects.raw("SELECT * FROM Users WHERE username = %s AND password = %s", [username, password])[0]

                # Store user info in session
                request.session['user_id'] = user.user_id
                request.session['username'] = user.username
                request.session['user_role'] = user.user_role
                return redirect('dashboard')
            except:
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
            # print("phone_number value:", len(phone_number), type(phone_number))
            if phone_number == "":
                phone_number = None
            # Check if passwords match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return render(request, 'register.html', {'form': form})

            # Check if username already exists
            if len(Users.objects.raw("SELECT * FROM Users WHERE username = %s", [username])) > 0:
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

            # Users.objects.raw("INSERT INTO Users(username, password, first_name, last_name, phone_number, user_role, outstanding_balance) VALUES (%s, %s, %s, %s, %s, 'registered', 0.00)", [username, password, first_name, last_name, phone_number])
            # Users.objects.raw("COMMIT")

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Users(username, password, first_name, last_name, phone_number, user_role, outstanding_balance) VALUES (%s, %s, %s, %s, %s, 'registered', 0.00)", [username, password, first_name, last_name, phone_number])

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

            if len(Books.objects.raw("SELECT * FROM Books WHERE title = %s AND author = %s AND publish_year = %s", [title, author, publish_year])) > 0:
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
            
            # Books.objects.raw("INSERT INTO Books(title, author, summary, genre, publish_year) VALUES (%s, %s, %s, %s, %s)", [title, author, summary, genre, publish_year])

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Books(title, author, summary, genre, publish_year) VALUES (%s, %s, %s, %s, %s)", [title, author, summary, genre, publish_year])


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
        pattern = f"%{query}%"
        books = Books.objects.raw("SELECT * FROM Books WHERE title LIKE %s OR author LIKE %s", [pattern, pattern])
    return render(request, 'search.html', {'books': books, 'query': query})

from django.db import connection
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages

def place_hold(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        user_id = request.session.get('user_id')

        if not user_id:
            messages.error(request, "You must be logged in to place a hold.")
            return redirect('search_books')

        try:
            with connection.cursor() as cursor:
                # Check if the book exists
                cursor.execute("SELECT title FROM Books WHERE book_id = %s", [book_id])
                book_row = cursor.fetchone()
                if not book_row:
                    messages.error(request, "Book not found.")
                    return redirect('search_books')
                book_title = book_row[0]

                # Check if user already has a hold on this book
                cursor.execute("""
                    SELECT 1 FROM Holds 
                    WHERE book_id = %s AND user_id = %s
                """, [book_id, user_id])
                existing = cursor.fetchone()

                if existing:
                    messages.info(request, f"You already have a hold on '{book_title}'.")
                else:
                    now = timezone.now()
                    cursor.execute("""
                        INSERT INTO Holds (book_id, user_id, hold_date)
                        VALUES (%s, %s, %s)
                    """, [book_id, user_id, now])
                    messages.success(request, f"Hold placed on '{book_title}'.")

        except Exception as e:
            messages.error(request, f"Error placing hold: {str(e)}")

    return redirect('search_books')
