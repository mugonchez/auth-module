from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class UserManager(BaseUserManager):
    '''
    create normal user
    '''
    def create_user(self, username, first_name, last_name, email, phone_number, password, **other_fields):
         
         email = self.normalize_email(email)
         user = self.model(email=email, 
                          username=username,
                          first_name=first_name,
                          last_name=last_name,
                          phone_number=phone_number,
                           **other_fields)
         user.set_password(password)
         user.save()
         return user
    
    '''
    create superuser
    '''
    def create_superuser(self, username, first_name, last_name, email, phone_number, password, **other_fields):
         email = self.normalize_email(email)
         other_fields.setdefault('is_staff', True)
         other_fields.setdefault('is_superuser', True)
         other_fields.setdefault('is_active', True)
         if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned staff privileges.')
         if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned superuser priviledges')

         return self.create_user(username, first_name, last_name, email, phone_number, password, **other_fields)


# user model
class User(AbstractUser):
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20,unique=True)
    profile_photo = models.FileField(upload_to=upload_to, null=True, blank=True)
    activation_link_expires_at = models.DateTimeField(blank=True, null=True)
    reset_password_link_expires_at = models.DateTimeField(blank=True, null=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']


    def __str__(self):
        return self.username
    


