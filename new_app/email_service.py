from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone

class EmailService():

    @staticmethod
    def sendRegisterEmail(request, user):
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Generate the password reset URL
        verify_url = reverse('verify_email', kwargs={
            'uidb64': uidb64,
            'token': token,
        })
        verify_url = request.build_absolute_uri(verify_url)

        EmailService.send_email(
            user.email,
            'Gaia verification',
            f'Please follow this link to verify your email: {verify_url}',
        )

    @staticmethod
    def sendPasswordResetEmail(request, user):
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Generate the password reset URL
        reset_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uidb64,
            'token': token,
        })
        reset_url = request.build_absolute_uri(reset_url)

        user.password_reset_timestamp = timezone.now()
        user.save()

        EmailService.send_email(
            user.email,
            'Password Reset',
            f'Please follow this link to reset your password: {reset_url}',
        )

    @staticmethod
    def send_email(emil, header, message):
        send_mail(
            header,
            message,
            'ori@gaialabs.ai',
            [emil],
            fail_silently=False,
        )