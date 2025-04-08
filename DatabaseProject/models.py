from django.db import models

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.TextField(unique=True)
    password = models.TextField()
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    phone_number = models.TextField(unique=True, null=True, blank=True)
    user_role = models.CharField(max_length=10)
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'DatabaseProject'
        db_table = 'users'
        managed = False

class Books(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.TextField()
    author = models.TextField()
    summary = models.TextField(null=True, blank=True)
    genre = models.TextField(null=True, blank=True)
    publish_year = models.IntegerField()

    class Meta:
        app_label = 'DatabaseProject'
        db_table = 'books'
        managed = False

class Copies(models.Model):
    copy_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Books, models.CASCADE, db_column='book_id')
    is_available = models.BooleanField()

    class Meta:
        app_label = 'DatabaseProject'
        db_table = 'copies'
        managed = False

class BalanceHistory(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, models.CASCADE, db_column='user_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_change = models.DateTimeField()

    class Meta:
        app_label = 'DatabaseProject'
        db_table = 'balance_history'
        managed = False

class Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    copy = models.ForeignKey(Copies, models.CASCADE, db_column='copy_id')
    user = models.ForeignKey(Users, models.CASCADE, db_column='user_id')
    checkout_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()

    class Meta:
        app_label = 'DatabaseProject'
        db_table = 'reservations'
        managed = False

class Holds(models.Model):
    hold_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Books, models.CASCADE, db_column='book_id')
    user = models.ForeignKey(Users, models.CASCADE, db_column='user_id')
    hold_date = models.DateTimeField()

    class Meta:
        app_label = 'DatabaseProject'
        db_table = 'holds'
        managed = False