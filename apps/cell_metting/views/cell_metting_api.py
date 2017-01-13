
from django.contrib.auth.models import User, Group

from cell_metting.serializers import CellMettingSerializer
from cell_metting.models import *


from rest_framework_mongoengine.viewsets import GenericViewSet, ModelViewSet

from rest_framework.response import Response



class CellMettingsViewSet(ModelViewSet):
	"""
	API endpoint that allows cells to be viewed or edited.
	"""
	queryset = Cell_mettings.objects.limit(2)
	serializer_class = CellMettingSerializer


	def list(self, request):
		queryset = self.queryset
		serializer = CellMettingSerializer(queryset, many=True)
		return Response(serializer.data)