from django import forms
from django.contrib import admin

from new_app.models import User
from new_app.app_models.company import Company
from new_app.app_models.user_privacy_model_prompt import UserPrivacyModelPrompt
from new_app.app_models.user_prompt import UserPrompt
from new_app.app_models.user_activity import UserActivity
from new_app.app_models.user_setting import UserSetting
from new_app.app_models.email_que import EmailQue
from new_app.app_models.company_admin import CompanyAdmin

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
UserAdmin.fieldsets += (('Extra Fields', {'fields': ('role','company', 'email_confirmed', )}),)
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
        return True

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
        return True

admin.site.register(UserPrivacyModelPrompt, UserPrivacyModelPromptForm)

class CompanyAdminForm(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user','company',)}),
    )

    list_display = ('user','company','created',)
    list_filter = ('user','company',)
    class Meta:
        model = CompanyAdmin
        fields = ('user','company',)

admin.site.register(CompanyAdmin, CompanyAdminForm)

class UserActivityForm(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user','prompt','ip_address',)}),
    )

    list_display = ("user", 'action_type', 'status', 'data','ip_address',)
    list_filter = ("user", 'action_type',)
    class Meta:
        model = UserActivity
        fields = ("user", 'action_type', 'status', 'data','ip_address',)
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(UserActivity, UserActivityForm)

class EmailQueForm(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('subject','message','recipient_list','sent',)}),
    )

    list_display = ('subject','message','recipient_list','sent',)
    list_filter = ("subject", 'sent',)
    class Meta:
        model = EmailQue
        fields = ('subject','message','recipient_list','sent',)
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(EmailQue, EmailQueForm)

class UserSettingsForm(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'key', 'data',)}),
    )

    list_display = ('user', 'key', 'data',)
    list_filter = ('user', 'key',)
    class Meta:
        model = UserSetting
        fields = ('user', 'key', 'data',)
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(UserSetting, UserSettingsForm)

