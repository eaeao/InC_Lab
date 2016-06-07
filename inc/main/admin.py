from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from inc.main.models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = True

class UserAdmin(UserAdmin):
    list_display = ('id','username','first_name','date_joined')
    inlines = [UserProfileInline]
    ordering = ('-id',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)