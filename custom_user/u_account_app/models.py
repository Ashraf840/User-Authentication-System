from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
# This model will consist of "create_user" & "create_superuser" functions
class MyUserManager(BaseUserManager):
    """ User Model Manager """
    def create_user(self, email, company_name, phone, password=None):
        # Check basic validation for the required fields inside "MyUser" class
        if not email:
            raise ValueError("Email is required!")
        if not company_name:
            raise ValueError("Company name is required!")
        if not phone:
            raise ValueError("Please provide an active phone number!")

        # Create the user in the model, then set the password for that user and saving the info in the model
        user = self.model(
            email=self.normalize_email(email),
            company_name=company_name,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, company_name, phone, password=None):
        user = self.create_user(
            email=email,
            company_name=company_name,
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    # User Info
    email = models.EmailField(verbose_name="Email Address", max_length=60, unique=True)
    company_name = models.CharField(verbose_name="Company Name", max_length=200, unique=True)
    phone = models.CharField(verbose_name="Company Phone", max_length=20)
    # Registration
    date_joined = models.DateTimeField(verbose_name="Date Join", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    # Permission /// will be appeared as a radio button, while creating a new user in the Django Admin Site
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Main Field for authentication
    USERNAME_FIELD = 'email'

    # When creating user account, the following fields must need to fill
    REQUIRED_FIELDS = ['company_name', 'phone']

    # Define the base user model manager
    objects = MyUserManager()

    class Meta():
        verbose_name_plural = "User List"

    def __str__(self):
        return self.company_name

    # While signing up, is going to have any permission that we're going to define later,
    # and when we're using group to define permission for the user, so it's thinking about if
    # the signing user is going to have any kind of permission, so this should just return True.
    # Return True, if the user has specified permission
    def has_perm(self, perm, obj=None):
        return True

    # The signup user will have permission to access other models in this app
    def has_module_perms(self, app_label):
        return True
