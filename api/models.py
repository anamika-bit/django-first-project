from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime    



# Create your models here.
BUSINESS_CHOICES = (("Individual","Individual"),("Corporate","Corporate"),("Proprietor","Proprietor"))

class Country(models.Model):
    country_name = models.CharField(max_length = 30, blank = False)
    country_code = models.CharField(max_length = 3, blank = False)
    def __str__(self):
        return self.country_name

class State(models.Model):
    country_id = models.ForeignKey(Country, on_delete = models.CASCADE)
    state_name = models.CharField(max_length = 30, blank = False)
    def __str__(self):
        return self.state_name

class City(models.Model):
    state_id = models.ForeignKey(State, on_delete = models.CASCADE)
    city_name = models.CharField(max_length = 30, blank = False)
    def __str__(self):
        return self.city_name


class UserManager(BaseUserManager):
    def create_user(self,email,name, password = None):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email = self.normalize_email(email),
            name = name,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    
    def create_staffuser(self, email, name, address, phone, business_type, city_id,state_id,country_id,country_code, password=None):
        if not name:
            raise ValueError("User must have a name")
        if not phone:
            raise ValueError("User must have a phone no.")
        if not city_id:
            raise ValueError("User must have a city_id")
        if not state_id:
            raise ValueError("User must have a state_id")
        if not country_id:
            raise ValueError("User must have a country_id")
        if not address:
            raise ValueError("User must have an address")
        if not business_type:
            raise ValueError("User must have a business_type")
        user = self.create_user(
            name = name,
            email = email,
            password = password
        )
        user.address = address
        user.business_type = business_type
        user.phone = phone
        user.city_id = city_id
        user.state_id = state_id
        user.country_id = country_id
        user.country_code = country_code
        user.is_staff = True
        user.save(using = self._db)
        return user


    def create_superuser(self,name , email,password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            name = name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length = 30, blank = False)
    email = models.EmailField(verbose_name = "email" , max_length = 30, unique = True, blank = False)
    business_type = models.CharField(max_length = 10, blank = False , choices = BUSINESS_CHOICES)
    phone = models.CharField(max_length = 10, validators=[MinLengthValidator(10)], blank = False)
    address = models.CharField(max_length = 30, blank = False)
    state_id = models.ForeignKey(State, on_delete = models.CASCADE, default = '1')
    city_id = models.ForeignKey(City, on_delete = models.CASCADE, default = '2')
    country_id = models.ForeignKey(Country, on_delete = models.CASCADE, default = '1')
    country_code = models.CharField(max_length = 3,validators=[MinLengthValidator(3)], blank = False)
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now = True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    hide_email = models.BooleanField(default = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm ,obj=None): 
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    