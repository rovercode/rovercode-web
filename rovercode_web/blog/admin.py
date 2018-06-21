"""Admin configuration for blog."""
from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    """Admin class for post model."""

    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
