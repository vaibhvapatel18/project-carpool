from django.contrib import admin
from app1.models import Data,Blog,Myride ,Rideinfo

# Register your models here.

admin.site.register(Blog)
admin.site.register(Myride)
admin.site.register(Rideinfo)

@admin.register(Data)
class UserAdmin(admin.ModelAdmin):
    list_display=['name','email','password']

# @admin.register(Blog)
# class UserAdmin(admin.ModelAdmin):
#     list_display=['tital','content']