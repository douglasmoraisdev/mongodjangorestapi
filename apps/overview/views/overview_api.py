from django.contrib.auth.models import User, Group

from overview.serializers import *
from overview.models import *

from rest_framework.response import Response

from rest_framework_mongoengine.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet		



class OverviewViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Overview.objects.all()
    serializer_class = OverviewSerializer    


    #Override
    def list(self, request):
        queryset = Overview.objects()
        serializer = OverviewSerializer(queryset, many=True)
        return Response(serializer.data)