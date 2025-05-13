from .models import Artist, Gallery, Booking
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


# Register your models here.


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "bio"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "session_date", "start_time", "status"]
    list_filter = ["status", "session_date", "start_time", "user"]
    search_fields = ["tattoo_description", "user"]
    ordering = ["status", "created_at"]


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "title", "description", "style"]
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ["title", "uploaded_at"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ['-created_at']
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'created_at')
    list_filter = ('is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

