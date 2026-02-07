from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'publish', 'status')
    list_filter = ('title', 'user', 'publish', 'status')
    list_editable = ('status',)
    raw_id_fields = ('user',)
    search_fields = ('title', 'description', 'user')
    ordering = ('-created', '-title')
    date_hierarchy = 'created'
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject')
    list_filter = ('name', 'email', 'phone', 'subject')
    list_editable = ('subject',)
    ordering = ('-name', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created', 'active')
    list_editable = ('active', 'post')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'post')
    