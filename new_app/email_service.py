from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone
from new_app.app_models.email_que import EmailQue
import threading
import os

main_sender = 'ori@gaialabs.ai'
disable_db = True

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
        if os.name == 'nt' or disable_db:  # for windows no cron jobs
            EmailService.send_email(
                [user.email],
                'Gaia verification',
                f'Please follow this link to verify your email: {verify_url}',
                main_sender
            )
        else:
            EmailService.add_email_to_db(
                subject='Gaia verification',
                message=f'Please follow this link to verify your email: {verify_url}',
                sender=main_sender,
                recipient_list=[user.email]
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

        if os.name == 'nt' or disable_db:  # for windows no cron jobs
            EmailService.send_email(
                [user.email],
                'Password Reset',
                f'Please follow this link to reset your password: {reset_url}',
                main_sender
            )
        else:
            EmailService.add_email_to_db(
                subject='Password Reset',
                message=f'Please follow this link to reset your password: {reset_url}',
                sender=main_sender,
                recipient_list=[user.email]
            )

    @staticmethod
    def send_email(recipient_list, subject, message, sender):
        send_mail(
            subject,
            message,
            sender,
            recipient_list,
            fail_silently=False,
        )

    @staticmethod
    def send_email_thread(email, subject, message):
        threading.Thread(

            # call to send_html_mail
            target=EmailService.send_email,

            kwargs={
                "recipient_list": [email],
                "subject": subject,
                "message": message,
                "sender": main_sender
            }).start()

    @staticmethod
    def add_email_to_db(subject, message, sender, recipient_list):
        EmailQue.objects.create(
            subject=subject,
            message=message,
            sender=sender,
            recipient_list=recipient_list
        )

    @staticmethod
    def set_sent(email_query_set: EmailQue, sent: bool):
        email_query_set.sent = sent
        email_query_set.save()
