from rest_framework import generics, permissions

class BaseUserAuthApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]