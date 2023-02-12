from django.contrib import admin

from new_app.models import User

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('role',)}),
    )

UserAdmin.list_display += ('role',)  # don't forget the commas
UserAdmin.list_filter += ('role',)
UserAdmin.fieldsets += (('Extra Fields', {'fields': ('role', )}),)
admin.site.register(User, UserAdmin)
