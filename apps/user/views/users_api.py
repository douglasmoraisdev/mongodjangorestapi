from django.contrib.auth.models import User, Group

from user.serializers import *
from user.models import *

from rest_framework.response import Response

from rest_framework_mongoengine.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet		



class UsersViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = BUsers.objects.all()
    serializer_class = UsersSerializer    


    #Override
    def list(self, request):
        queryset = BUsers.objects().limit(4)
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data)