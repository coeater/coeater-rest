from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from rest_framework_jwt.settings import api_settings

import uuid

class UserManager(BaseUserManager):
    """
    Manage creating user and superuser
    """
    use_in_migrations = True

    def create_user(self, uid, nickname, password=None):
        if not uid :
            raise ValueError('must have user uid')
        user = self.model(uid=uid, nickname=nickname)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, jwt, uid, nickname, password):
        user = self.create_user(uid=uid, nickname=nickname, password = password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        code = uuid.uuid4().hex[:6].upper()

        user.jwt = token
        user.code = code
        user.set_password(password)
        user.save(using=self._db)

        return user

class User(AbstractBaseUser,PermissionsMixin):
    objects = UserManager()

    #firebase id
    uid = models.CharField(unique=True, null=False, blank=False, max_length=300)

    #token
    jwt = models.CharField(unique=True, null=True, blank=True, max_length=300)

    #friend code
    code = models.CharField(unique=True, null=True, blank=True, max_length=10)

    #displayed name
    nickname = models.CharField(unique=True, null=False, blank=False, max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    #Data used internally
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['jwt', 'nickname']

class Friend(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friended")

class History(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="histories")
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="historied")