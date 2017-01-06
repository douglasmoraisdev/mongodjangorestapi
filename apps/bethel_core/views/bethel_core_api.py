from django.contrib.auth.models import User, Group

from bethel_core.serializers import *
from bethel_core.models import *

from rest_framework.response import Response

from rest_framework_mongoengine.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet		



class BethelCoreViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Users.objects.all()
    serializer_class = BethelCoreSerializer    


    #Override
    def list(self, request):
        queryset = Users.objects()
        serializer = BethelCoreSerializer(queryset, many=True)
        return Response(serializer.data)