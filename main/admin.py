from django.contrib import admin
from .models import CustomUser, DataItemSetModel, ImageModel


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "unique_code",
        "user_email",
        "allow_promotional",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    ]


@admin.register(DataItemSetModel)
class DataItemSetModelAdmin(admin.ModelAdmin):
    list_display = [
        "user_code",
        "item_set_heading",
        "set_items",
        "color",
        "font_name",
        "font_size",
        "position_x_y",
    ]

    def set_items(self, obj):
        if len(obj.item_set) >= 25:
            return f"{obj.item_set[:25]}..."
        else:
            return obj.item_set

    def position_x_y(self, obj):
        return f"x:{obj.position_x} y:{obj.position_y}"


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = [
        "get_user_username",
        "image_file_name",
        "image_url",
        "exports",
        "export_image_count",
    ]

    def image_url(self, obj):
        return obj.image.url if obj.image else "No Image"

    def get_user_username(self, obj):
        return obj.user.username
