from django.contrib import admin
import django_jalali.admin as jadmin

from .models import *


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'username', 'date', 'featured')
    search_fields = ('title',)
    list_filter = ('featured',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('cm_date', 'author', 'post')
    list_filter = ('cm_date',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    ordering = ['date']
    list_display = ('title', 'date', 'description', 'link')
    list_editable = ('date',)
    list_filter = ('date',)
    search_fields = ('title',)


admin.site.register(Attachment)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_honored')
    list_editable = ('is_honored',)
    list_filter = ('is_honored',)
    search_fields = ('title',)

# admin.site.register(Category)
