from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.middleware.csrf import get_token
from django.forms.models import model_to_dict
from knox.models import AuthToken
from new_app.serializers import UserSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer, ForgotPasswordSerializer, MyAuthTokenSerializer, MyEmailSerializer
from knox.views import LoginView as KnoxLoginView
from new_app.api.jsonResponse import baseHttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.core.mail import send_mail

token_delta = relativedelta(days=1)
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=False)
        response = baseHttpResponse()
        if valid:
            user = serializer.save()
            obj = {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
                "csrftoken": get_token(request),
                "csrftoken_exp": (datetime.now() + token_delta).replace(microsecond=0),
            }
            response.data = obj
            return Response(response.dict())
        else:
            response.err = 1
            error_list = [serializer.errors[error][0] for error in serializer.errors]
            response.errMessage = error_list
            return Response(response.dict())

# Login API

class LoginAPI(generics.GenericAPIView):
    # authentication_classes = [BasicAuthentication]
    serializer_class = LoginSerializer

    @method_decorator(csrf_exempt, name='post')
    def post(self, request, *args, **kwargs):
        print('request', request)
        serializer = MyAuthTokenSerializer(data=request.data)
        valid = serializer.is_valid(raise_exception=False)
        response = baseHttpResponse()
        if valid:
            user = serializer.validated_data['user']
            login(request, user)
            obj = {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
                "csrftoken": get_token(request),
                # "csrftoken_exp": (datetime.now() + relativedelta(years=1)).replace(microsecond=0),
                "csrftoken_exp": (datetime.now() + token_delta).replace(microsecond=0),
            }
            response.data = obj
            return Response(response.dict())
        else:
            response.err = 1
            response.errMessage = 'Unable to log in with provided credentials.'
            return Response(response.dict())

class LogoutAPI(generics.GenericAPIView):
    # authentication_classes = [BasicAuthentication]
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






