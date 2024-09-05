from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Call)
admin.site.register(Participant)
admin.site.register(ChatMessage)


admin.site.register(Invitation)
