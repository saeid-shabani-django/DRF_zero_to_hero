from django.contrib import admin

from core.models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display =['id','username','first_name','last_name','email']


