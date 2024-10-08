from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User




class Book(models.Model):
    title = models.CharField(max_length=150,null=False)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    number_of_copies_available = models.PositiveIntegerField()


    
class LibraryUser(models.Model):

    date_of_membership = models.DateField(auto_now_add=True)
    active_status = models.BooleanField(default=True)


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='library_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
 
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='library_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)