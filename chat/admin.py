from django.contrib import admin

from chat.models import Message, Room

# Register your models here.
@admin.register(Room)
class AdminRoom(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['content']
  