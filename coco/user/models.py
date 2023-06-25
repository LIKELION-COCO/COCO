from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, username, age, **kwargs):
        user = self.model(email=email, username=username, age=age, **kwargs)
        user.set_password(password)
        user.save()

    def create_normaluser(self, email, password, username, age, **kwargs):
        self.create_user(email, password, username, age, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_superuser", True)
        username = 'root'
        age = 0
        self.create_user(email, password, username, age, **kwargs)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True, max_length=30)
    username = models.CharField(max_length=20)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_staff(self):
        return self.is_superuser

class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, to_field='email', db_constraint=False)
    nickname = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='profile/', null=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.nickname
