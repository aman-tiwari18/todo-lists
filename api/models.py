from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from api.utils import UsernameValidator, validate_username


class AccountManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not validate_username(username) or (not username):
            raise ValueError("Invalid Username")
        account = self.model(username=username, **extra_fields)
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, password, **extra_fields)


class Account(AbstractBaseUser):
    username_validator = UsernameValidator()
    username = models.CharField(
        unique=True, blank=False, validators=[username_validator], max_length=20
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    objects = AccountManager()


class TodoList(models.Model):
    name = models.CharField(max_length=120, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    account = models.ForeignKey(
        Account, related_name="user_todo_list", on_delete=models.CASCADE, blank=False
    )

    class Meta:
        ordering = ["created_at"]


class Task(models.Model):
    name = models.CharField(max_length=120, blank=False)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    todo_list = models.ForeignKey(
        TodoList, related_name="user_todo", on_delete=models.CASCADE, blank=False
    )

    class Meta:
        ordering = ["created_at"]
