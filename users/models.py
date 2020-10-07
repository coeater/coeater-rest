from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

class UserManager(BaseUserManager):
    """
    Manage creating user and superuser
    """
    use_in_migrations = True

    def create_user(self, phone, nickname, password=None):
        if not phone :
            raise ValueError('must have user phone')
        user = self.model(phone = phone, nickname = nickname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, nickname, password):
        user = self.create_user(
                phone = email,
                nickname = nickname,
                password = password
                )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    objects = UserManager()

    phone = PhoneNumberField(
            null=False,
            blank=False,
            unique=True,
            )
    nickname = models.CharField(
            max_length=20,
            null=False,
            blank=False,
            unique=True
            )
    created = models.DateTimeField(auto_now_add=True, editable=False)

    #Data used internally
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['nickname']

class Friend(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")

class History(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="histories")
