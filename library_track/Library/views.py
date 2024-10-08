from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, LibraryUser, Transaction
from .serializers import BookSerializer, LibraryUserSerializer, TransactionSerializer

from django.utils import timezone

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        books = Book.objects.filter(number_of_copies_available__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

class LibraryUserViewSet(viewsets.ModelViewSet):
    queryset = LibraryUser.objects.all()
    serializer_class = LibraryUserSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')

        try:
            user = LibraryUser.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)
        except (LibraryUser.DoesNotExist, Book.DoesNotExist):
            return Response({'error': 'User or Book not found'}, status=status.HTTP_404_NOT_FOUND)

        if book.number_of_copies_available <= 0:
            return Response({'error': 'No available copies'}, status=status.HTTP_400_BAD_REQUEST)

        if Transaction.objects.filter(user=user, book=book, return_date__isnull=True).exists():
            return Response({'error': 'Book already checked out by this user'}, status=status.HTTP_400_BAD_REQUEST)

        Transaction.objects.create(user=user, book=book)
        book.number_of_copies_available -= 1
        book.save()

        return Response({'message': 'Book checked out successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def return_book(self, request):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')

        try:
            user = LibraryUser.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)
            transaction = Transaction.objects.filter(user=user, book=book, return_date__isnull=True).first()
        except (LibraryUser.DoesNotExist, Book.DoesNotExist):
            return Response({'error': 'User or Book not found'}, status=status.HTTP_404_NOT_FOUND)

        if not transaction:
            return Response({'error': 'No active transaction found'}, status=status.HTTP_400_BAD_REQUEST)

        transaction.return_date = timezone.now()
        transaction.save()
        book.number_of_copies_available += 1
        book.save()

        return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)
 
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import logout

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})

class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
