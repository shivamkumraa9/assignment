from django.contrib import admin

from accounts.models import MyUser,UserAuth


admin.site.register(MyUser)
admin.site.register(UserAuth)
