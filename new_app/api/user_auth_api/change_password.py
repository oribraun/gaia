# Change Password
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from new_app.serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from .base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse

class ChangePasswordApi(BaseUserAuthApi):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    # permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = baseHttpResponse()
            response.status = status.HTTP_200_OK
            response.code = 'success'
            response.message = 'Password updated successfully'
            response.data = []

            return Response(response.dict())

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)