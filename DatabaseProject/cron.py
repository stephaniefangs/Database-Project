from django.db import connection
from .models import Reservations
from django.db import connection

def increment_fees():
    overdue_books = Reservations.objects.raw("SELECT * FROM reservations WHERE CURRENT_DATE > reservations.due_date")
    for book in overdue_books:
        with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE users
                    SET outstanding_balance = outstanding_balance + 0.25
                    WHERE users.user_id = %s                  
                """, [book.user_id])
    return