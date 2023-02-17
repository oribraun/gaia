from django import forms
from django.contrib import admin

from new_app.models import User
from new_app.app_models.company import Company
from new_app.app_models.user_privacy_model_prompt import UserPrivacyModelPrompt
from new_app.app_models.user_prompt import UserPrompt

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

UserAdmin.list_display += ('role','company','created','modified',)  # don't forget the commas
UserAdmin.list_filter += ('role','company',)
UserAdmin.fieldsets += (('Extra Fields', {'fields': ('role','company', )}),)
admin.site.register(User, UserAdmin)


class CompanyForm(admin.ModelAdmin):
    name = forms.CharField(max_length=100)

    fieldsets = (
        (None, {'fields': ('name','domain',)}),
    )

    list_display = ("name",'domain','key',)
    class Meta:
        model = Company
        fields = ("name",'domain',)

    def save(self, commit=True):
        company = super(CompanyForm, self).save(commit=False)
        # company.name = self.cleaned_data['name']
        if commit:
            company.save()
        return company

admin.site.register(Company, CompanyForm)

class UserPromptsForm(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user','prompt','ip_address',)}),
    )

    list_display = ("user",'prompt','ip_address',)
    list_filter = ('user','ip_address',)
    class Meta:
        model = UserPrompt
        fields = ("user",'prompt','ip_address',)
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(UserPrompt, UserPromptsForm)

class UserPrivacyModelPromptForm(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user','prompt','company','ip_address','created',)}),
    )

    list_display = ("user",'prompt','company','ip_address','created',)
    list_filter = ('user','company','ip_address',)
    class Meta:
        model = UserPrivacyModelPrompt
        fields = ("user",'prompt','company','ip_address','created',)
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(UserPrivacyModelPrompt, UserPrivacyModelPromptForm)