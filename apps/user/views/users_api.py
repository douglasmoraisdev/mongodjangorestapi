from django.contrib.auth.models import User, Group

from user.serializers import *
from user.models import *

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_mongoengine.viewsets import ModelViewSet

from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope



class UsersViewSet(ProtectedResourceView, ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = BUsers.objects.all()
    serializer_class = UsersSerializer    


    # OAuth
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    required_scopes = ['cells']

    #Override
    def list(self, request):
        queryset = BUsers.objects().limit(4)
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data)