from rest_framework import serializers
from .models import Book, User, Transaction
from django.contrib.auth.models import User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  '__all__'
       

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LibraryUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        Library_user = User.objects.create(user=user, **validated_data)
        return Library_user

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
