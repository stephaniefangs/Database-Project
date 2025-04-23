from django.db import connection
from .models import Reservations
from django.db import connection

def increment_fees():
    overdue_books = Reservations.objects.raw("SELECT * FROM reservations WHERE CURRENT_DATE > reservations.due_date AND reservations.return_date IS NULL")
    with connection.cursor() as cursor:
        for book in overdue_books:
            cursor.execute("""
                UPDATE users
                SET outstanding_balance = outstanding_balance + 0.25
                WHERE users.user_id = %s                  
            """, [book.user_id])
    return