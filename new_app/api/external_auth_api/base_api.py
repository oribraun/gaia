from rest_framework import generics, permissions

class BaseExternalAuthApi(generics.RetrieveAPIView):
    pass
    # permission_classes = [permissions.IsAuthenticated,]