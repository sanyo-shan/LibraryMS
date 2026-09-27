from .models import Book, Member, Loan, Reservation, Librarian, Fine
from rest_framework import serializers
from django.contrib.auth.models import User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'total_copies', 'available_copies', 'cover_image']

    def validate_available_copies(self, value):
        if value.available_copies < 0:
            raise serializers.ValidationError("Available copies cannot be negative.")
        if value > self.total_copies:
            raise serializers.ValidationError("Available copies cannot exceed total copies.")
        return value

class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)
    first_name = serializers.CharField(source='user.first_name', max_length=30, required=True)
    last_name = serializers.CharField(source='user.last_name', max_length=30, required=False)
    is_staff = serializers.BooleanField(source='user.is_staff', default=False)
    
    class Meta:
        model = Member
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 
                  'membership_date', 'fines_due', 'is_staff', 'password']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            password=validated_data.pop('password'),
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            is_staff=user_data.get('is_staff', False)
        )

        member = Member.objects.create(user=user, **validated_data)
        return member

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'book', 'member', 'loan_date', 'due_date', 'is_returned', 
                  'returned_date', 'status']

    # def validate(self, data):
    #     if data['is_returned'] and not data['returned_date']:
    #         raise serializers.ValidationError("Returned date must be set if the book is marked as returned.")
    #     return data

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'member', 'book', 'created_at', 'cancel_flag', 'fulfilled_flag']

    def validate(self, data):
        if data.get('cancel_flag') and data.get('fulfilled_flag'):
            raise serializers.ValidationError("A reservation cannot be both canceled and fulfilled.")
        return data

class LibrarianSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Librarian
        fields = ['id', 'user', 'can_add_book', 'can_edit_book', 'can_remove_book', 'can_manage_members', ''
        'can_manage_loans', 'can_manage_reservations', 'username', 'password']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=user_data['username'], password=password, is_staff=True)
        
        librarian = Librarian.objects.create(user=user, **validated_data)
        return librarian

class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = ['id', 'member', 'amount', 'issued_date', 'paid_flag']

    