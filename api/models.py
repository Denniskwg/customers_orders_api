from django.db import models
import uuid
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import MinValueValidator, MinLengthValidator


def generate_uuid():
    """generates unique string id
    """
    return str(uuid.uuid4())

def get_time():
    return timezone.now()

class BaseModel(models.Model):
    """base class to be inherited by user model. Ensures each user object has a unique id
    """
    id = models.CharField(max_length=60, primary_key=True, default=generate_uuid, editable=False)
    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    """custom user manager for creating regular users and admin users
    """
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        try:
            user = self.model(username=username, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except IntegrityError:
            raise ValueError('User with this username already exists')

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, **extra_fields)


class Customer(BaseModel):
    name = models.CharField(max_length=60, unique=True)
    code = models.CharField(max_length=60, default=generate_uuid)
    phone_number = models.CharField(max_length=60, unique=True)
    class Meta:
         db_table = 'customers'


class Order(BaseModel):
    time = models.DateTimeField(null=False, default=get_time)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
    item = models.CharField(max_length=60, validators=[MinLengthValidator(1)])
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='orders')
    class Meta:
         db_table = 'orders'

class User(AbstractUser, BaseModel):
    """custom user class
    """
    email = None
    first_name = None
    last_name = None
    username = models.CharField(max_length=30, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
    class Meta:
        db_table = 'users'
