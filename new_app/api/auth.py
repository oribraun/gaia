from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.forms.models import model_to_dict
from knox.models import AuthToken
from new_app.serializers import UserSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer, ForgotPasswordSerializer, MyAuthTokenSerializer, MyEmailSerializer
from knox.views import LoginView as KnoxLoginView
from django.core.mail import send_mail

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @method_decorator(ensure_csrf_cookie, name='post')
    def post(self, request, *args, **kwargs):
        serializer = MyAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
            # "csrf_token": csrf_token
        })

class LogoutAPI(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({
            "success": True
        })

class ForgotPasswordAPI(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = MyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Generate the password reset URL
        reset_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uidb64,
            'token': token,
        })
        reset_url = self.request.build_absolute_uri(reset_url)

        user.password_reset_timestamp = timezone.now()
        user.save()
        # print('reset_url', reset_url)
        # Send the password reset email
        # send_mail(
        #     'Password Reset',
        #     f'Please follow this link to reset your password: {reset_url}',
        #     'noreply@example.com',
        #     [user.email],
        #     fail_silently=False,
        # )
        return Response({
            "err": 0,
            "errMessage": "",
            "reset_url": reset_url
        })

class LoginAPI1(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)






