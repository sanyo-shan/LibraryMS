from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=100)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def __str__(self):
        return self.title

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    membership_date = models.DateField(auto_now_add=True)
    fines_due = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)
    returned_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('BORROWED', 'Borrowed'),
            ('RETURNED', 'Returned'),
            ('OVERDUE', 'Overdue'),
        ],
        default='BORROWED'
    )

    def __str__(self):
        return f"{self.book.title} loaned to {self.member.first_name} {self.member.last_name}"

class Reservation(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cancel_flag = models.BooleanField(default=False)
    fulfilled_flag = models.BooleanField(default=False)

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    can_add_book = models.BooleanField(default=True)
    can_edit_book = models.BooleanField(default=True)
    can_remove_book = models.BooleanField(default=True)
    can_manage_members = models.BooleanField(default=True)
    can_manage_loans = models.BooleanField(default=True)
    can_manage_reservations = models.BooleanField(default=True)

class Fine(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    issued_date = models.DateField(auto_now_add=True)
    paid_flag = models.BooleanField(default=False)