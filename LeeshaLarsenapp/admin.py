from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
class cartitemadmin(admin.ModelAdmin):
    list_display=['product','order','quanity','date_added','user']
    def user(self,obj):
        return obj.order.user
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(order)
admin.site.register(cartitem,cartitemadmin)
admin.site.register(Product)

