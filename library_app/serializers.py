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
    
    class Meta:
        model = Member
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 
                  'membership_date', 'fines_due', 'password']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            password=validated_data.pop('password'),
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
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

# Addon
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
        fields = ['id', 'user', 'username', 'password']

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


# ********* Front Page Serializers *********

class MemberRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    def username_exists(self, username):
        return User.objects.filter(username=username).exists()

    def password_is_valid(self, password):
        return len(password) >= 8  # Example validation, adjust as needed

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        user.set_password(password)
        member = Member.objects.create(user=user)
        member.save()
        return member

class LibrarianRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    def username_exists(self, username):
        return User.objects.filter(username=username).exists()

    def password_is_valid(self, password):
        return len(password) >= 8  # Example validation, adjust as needed

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, is_staff=True)
        user.set_password(password)
        librarian = Librarian.objects.create(user=user)
        librarian.save()
        return librarian

class MemberLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            member = Member.objects.get(user__username=username)
            if not member.user.check_password(password):
                raise serializers.ValidationError("Invalid credentials")
        except Member.DoesNotExist:
            raise serializers.ValidationError("Member not found")

        return data

class LibrarianLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            librarian = Librarian.objects.get(user__username=username)
            if not librarian.user.check_password(password):
                raise serializers.ValidationError("Invalid credentials")
        except Librarian.DoesNotExist:
            raise serializers.ValidationError("Librarian not found")

        return data