from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

import os


class CustomUserManager(BaseUserManager):
    def create_user(self, user_email, password=None, **extra_fields):
        if not user_email:
            raise ValueError("The Email field must be set")
        user = self.model(user_email=self.normalize_email(user_email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("first_name", str(user_email.split("@")[0]))
        extra_fields.setdefault("last_name", "admin")
        return self.create_user(user_email, password, **extra_fields)


class CustomUser(AbstractUser):
    user_id = models.BigAutoField(primary_key=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        related_query_name="customuser_group",
        blank=True,
        verbose_name="groups",
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        related_query_name="customuser_permission",
        blank=True,
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
    )
    user_email = models.EmailField(
        max_length=255,
        verbose_name="User Email",
        unique=True,
        blank=True,
    )
    unique_code = models.CharField(
        max_length=4,
        editable=False,
        unique=True,
        null=False,
    )

    allow_promotional = models.BooleanField(
        blank=False, default=False, editable=True, null=False
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "user_email"
    EMAIL_FIELD = "user_email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.unique_code:
            unique_code = get_random_string(
                length=4, allowed_chars="bcfghklmopqrsuwxyz0123456789"
            )

            while CustomUser.objects.filter(unique_code=unique_code).exists():
                unique_code = get_random_string(
                    length=4, allowed_chars="bcfghklmopqrsuwxyz0123456789"
                )

            self.unique_code = unique_code

        if not self.username:
            self.username = f"{self.first_name}-{self.last_name}-{self.unique_code}"

        super().save(*args, **kwargs)

    def update_password(self, new_password):
        self.set_password(new_password)
        self.save()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Custom Users"


class DataItemSetModel(models.Model):
    item_set_id = models.AutoField(primary_key=True)

    item_set_heading = models.CharField(
        max_length=255,
        verbose_name="Item Data Set Heading",
    )
    item_set = models.TextField(
        verbose_name="Item Data Set List",
        default="[""]"
    )

    position_x = models.PositiveIntegerField(
        default=0,
    )
    position_y = models.PositiveIntegerField(
        default=0,
    )
    font_size = models.PositiveIntegerField(
        default=12,
    )
    font_name = models.CharField(
        max_length=255,
        unique=False,
        default="arial",
        verbose_name="Font Name",
    )
    color = models.CharField(
        max_length=9,
        unique=False,
        default="#aa33ffff",
        verbose_name="Text Color",
    )

    user_code = models.CharField(
        max_length=4,
        editable=False,
        unique=False,
        null=False,
    )
    created = models.DateTimeField(
        null=True,
    )

    # @staticmethod
    def search_font(font_name):
        font_path = os.path.join("static", "fonts", f"{font_name}.ttf")

        if os.path.exists(font_path):
            return font_path
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        if len(self.item_set) >= 25:
            return f"{self.item_set[:25]}..."
        else:
            return self.item_set

    class Meta:
        verbose_name_plural = "DataItem Set Models"


class ImageModel(models.Model):
    image_id = models.AutoField(primary_key=True)

    image_file_name = models.CharField(
        max_length=256,
        verbose_name="Image Name",
    )
    
    image_url = models.TextField(
        verbose_name="Image URL",
    )
    
    export_image_count = models.PositiveIntegerField(
        default=0,
    )
    exports = models.PositiveIntegerField(
        default=0,
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    def delete(self, *args, **kwargs):
        if self.image:
            storage, path = self.image.storage, self.image.path
            storage.delete(path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.image_file_name

    class Meta:
        verbose_name_plural = "Image Models"
