import re
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from django.core import exceptions
from django.contrib.auth import password_validation
from new_app.app_models.company import Company
User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display')
    company_name = serializers.CharField(source='company')
    # full_name = serializers.CharField(source='get_full_name')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'role_display', 'company_name')
        # fields = ('id', 'username', 'email', 'role', 'groups', 'last_login', 'full_name')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        domain = email[email.index('@') + 1:]
        company = None
        try:
            company = Company.objects.get(domain=domain)
        except:
            pass
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            company=company
        )

        return user

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

# Login Serializer
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'email': {'required': True,'allow_blank': False, 'label': 'Username or email'},
            'password': {'write_only': True},
        }

class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()
        extra_kwargs = {'password': {'write_only': True}}

class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email')

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class AuthCustomTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    extra_kwargs = {
        'email': {'required': True, 'allow_blank': True},
        'username': {'required': True, 'allow_blank': True},
        'password': {'write_only': True},
    }
    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')
        if (email or username) and password:
            # Check if user sent email
            if validateEmail(email):
                user_request = get_object_or_404(
                    User,
                    email=email,
                )

                username = user_request.username

            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email or username" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


def validateEmail(email):
    if len(email) > 6:
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, email):
            return 1
    return 0


class MyAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Username or email"),
        write_only=True,
        allow_blank=False,
    )

    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        # username = attrs.get('username')
        username = None
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            # Check if user sent email
            if validateEmail(email):
                # username = get_object_or_404(User, email=username)
                try:
                    username = User.objects.get(email__exact=email)
                except:
                    pass

            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class MyEmailSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True,
        allow_blank=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        if validateEmail(email):
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                msg = _('not a valid email address.')
                raise serializers.ValidationError(msg, code='valid email')
            attrs['user'] = user
            return attrs
        else:
            msg = _('not a valid email address.')
            raise serializers.ValidationError(msg, code='valid email')