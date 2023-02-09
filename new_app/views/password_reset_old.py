from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView

class PasswordResetView(FormView):
    template_name = 'password_reset.html'
    success_url = '/'
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.form_invalid(form)

        # Generate a token for password reset
        token = default_token_generator.make_token(user)

        # Generate the password reset URL
        reset_url = reverse('password_reset_confirm', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
        reset_url = self.request.build_absolute_uri(reset_url)

        # Send the password reset email
        send_mail(
            'Password Reset',
            f'Please follow this link to reset your password: {reset_url}',
            'noreply@example.com',
            [user.email],
            fail_silently=False,
        )

        return super().form_valid(form)