from django.shortcuts import render
from .serializers import (BookSerializer, FineSerializer,
             MemberSerializer, LoanSerializer, ReservationSerializer, LibrarianSerializer)
from .models import Book, Member, Loan, Reservation, Librarian, Fine
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

class BookListViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset

@permission_classes([IsAuthenticated])
class MemberListViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer

    def get_queryset(self):
        queryset = Member.objects.all()
        return queryset

@api_view(['POST'])
class MemberLogin(viewsets.ViewSet):
    serializer_class = MemberSerializer

    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            member = Member.objects.get(user__username=username)
            if member.user.check_password(password):
                serializer = self.serializer_class(member)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated])
class LoanListViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer

    def get_queryset(self):
        queryset = Loan.objects.all()
        return queryset


@permission_classes([IsAuthenticated])
class ReservationListViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = Reservation.objects.all()
        return queryset

class LibrarianListViewSet(viewsets.ModelViewSet):
    serializer_class = LibrarianSerializer

    def get_queryset(self):
        queryset = Librarian.objects.all()
        return queryset

@api_view(['POST'])
class LibrarianLogin(viewsets.ViewSet):
    serializer_class = LibrarianSerializer

    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            librarian = Librarian.objects.get(user__username=username)
            if librarian.user.check_password(password):
                serializer = self.serializer_class(librarian)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Librarian.DoesNotExist:
            return Response({'error': 'Librarian not found'}, status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated])
class FineListViewSet(viewsets.ModelViewSet):
    serializer_class = FineSerializer

    def get_queryset(self):
        queryset = Fine.objects.all()
        return queryset


# ************ New Code **************
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (MemberLoginSerializer, LibrarianLoginSerializer,
                            MemberRegisterSerializer, LibrarianRegisterSerializer)
from django.contrib.auth.models import User
from django.shortcuts import redirect

@api_view(['GET'])
def login(request):
    return render(request, 'login.html')

@api_view(['POST']) # Allows API to accept POST requests
def member_login(request):
    if request.method == 'POST': 
        data = request.data # Contains the JSON sent by the client
        memberLoginSerializer = MemberLoginSerializer(data=data) # Passes the JSON to the serializer for validation
        if memberLoginSerializer.is_valid():
            username = memberLoginSerializer.validated_data['username'] # Retrieves the validated username
            member = Member.objects.get(user__username=username) # Retrieves the member object from the database
            refresh = RefreshToken.for_user(member.user) # Generates a JWT refresh token for the member
            return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token), # Generates a JWT access token for the member
                    }, status=status.HTTP_200_OK)
            # return render(request, 'home.html', {'member': member}) # Renders the home page with the member object

    return Response(memberLoginSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def librarian_login(request):
    if request.method == 'POST':
        data = request.data
        librarianLoginSerializer = LibrarianLoginSerializer(data=data)
        if librarianLoginSerializer.is_valid():
            username = librarianLoginSerializer.validated_data['username']
            librarian = Librarian.objects.get(user__username=username)
            refresh = RefreshToken.for_user(librarian.user)
            # return Response({
            #             'refresh': str(refresh),
            #             'access': str(refresh.access_token),
            #         }, status=status.HTTP_200_OK)
            response = Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

            if response.status_code == 200:
                # print(type(response))
                tokens = response.data
                print(response.data)

                request.session['access_token'] = tokens['access']
                request.session['refresh_token'] = tokens['refresh']

                return redirect('home')  # Redirect to the home page after successful login

    return Response(librarianLoginSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
def member_register(request):
    if request.method == 'GET':
        return render(request, 'memberRegister.html') # Renders the member registration page
    if request.method == 'POST':
        data = request.data
        memberRegisterSerializer = MemberRegisterSerializer(data=data)
        if memberRegisterSerializer.is_valid():
            memberRegisterSerializer.save() # Calls the create method in the serializer to create a new member
            return Response({'message': 'Member registered successfully'}, status=status.HTTP_201_CREATED)

        return Response(memberRegisterSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
def librarian_register(request):
    if request.method == "GET":
        return render(request, 'librarianRegister.html')

    if request.method == 'POST':
        data = request.data
        librarianRegisterSerializer = LibrarianRegisterSerializer(data=data)
        if librarianRegisterSerializer.is_valid():
            librarianRegisterSerializer.save() # Calls the create method in the serializer to create a new librarian
            return Response({'message': 'Librarian registered successfully'}, status=status.HTTP_201_CREATED)

        return Response(librarianRegisterSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def home(request):
    print(request.user)
    # print(request.header)
    print(request)
    return render(request, 'home.html')

@api_view(['POST'])
def logout(request):
    request.session.flush()
    return redirect('login')