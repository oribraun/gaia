from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView
from django.shortcuts import render
from django.conf import settings
from django import forms

UserModel = get_user_model()

class PasswordResetConfirmForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class PasswordResetConfirmView(FormView):
    template_name = 'password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = '/login'

    @method_decorator(csrf_protect)
    def get(self, request, *args, **kwargs):
        self.user = None
        self.token = kwargs.get('token')
        self.uidb64 = kwargs.get('uidb64')
        self.validlink = False

        try:
            uid = urlsafe_base64_decode(self.uidb64)
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            pass

        # Check if the link has expired
        default = 10 * 60 * 5  # 10 minutes
        expiration_time = getattr(settings, 'PASSWORD_RESET_EXPIRATION_TIME', default)
        expiration_diff = (timezone.now() - self.user.password_reset_timestamp).total_seconds()
        print((timezone.now() - self.user.password_reset_timestamp).total_seconds())
        if self.user is not None and default_token_generator.check_token(self.user, self.token) \
                and expiration_diff <= expiration_time:
            self.validlink = True

        if not self.validlink:
            # return render(request, 'password_reset_invalid.html')
            form = self.get_form()
            return self.form_invalid()

        return super().get(request, *args, **kwargs)

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        self.user = None
        self.token = kwargs.get('token')
        self.uidb64 = kwargs.get('uidb64')
        self.validlink = False

        try:
            uid = urlsafe_base64_decode(self.uidb64)
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            pass

        # Check if the link has expired
        default = 10 * 60 * 5 # 10 minutes
        expiration_time = getattr(settings, 'PASSWORD_RESET_EXPIRATION_TIME', default)
        expiration_diff = (timezone.now() - self.user.password_reset_timestamp).total_seconds()
        print('self.user', self.user)
        print('default_token_generator.check_token(self.user, self.token)', default_token_generator.check_token(self.user, self.token))
        if self.user is not None and default_token_generator.check_token(self.user, self.token):
            self.validlink = True

        if not self.validlink:
            # return render(request, 'password_reset_invalid.html')
            form = self.get_form()
            return render(self.request, 'password_reset_invalid.html', {'login_url': '/login/forgot'})
            # raise ValidationError('Password reset link is invalid.')

        print('self.validlink', self.validlink)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

from django.views.decorators.debug import sensitive_post_parameters
from django.contrib import messages

class PasswordResetConfirmView2(FormView):
    template_name = 'password_reset_confirm.html'
    form_class = PasswordResetConfirmForm
    success_url = '/login/'

    @method_decorator(sensitive_post_parameters('password', 'password_confirm'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.user = self.get_user(kwargs['uidb64'])
        if self.user is None:
            messages.error(self.request, 'Invalid reset link')
            # return redirect('password_reset')
        if not self.token_generator.check_token(self.user, kwargs['token']):
            messages.error(self.request, 'Invalid reset link')
            # return redirect('password_reset')
        return super().dispatch(request, *args, **kwargs)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes a string of the format
            # urlsafe_base64 to bytestring
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        return user

    def form_valid(self, form):
        self.user.set_password(form.cleaned_data['password'])
        self.user.save()
        messages.success(self.request, 'Password reset successful')
        return super().form_valid(form)