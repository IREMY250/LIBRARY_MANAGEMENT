from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, LibraryUserViewSet, TransactionViewSet, CustomAuthToken, LogoutView

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', LibraryUserViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
