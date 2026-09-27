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
