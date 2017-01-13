from .models import Cells

from user.models import User_roles

from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

from user.serializers import UserroleSerializer



class CellSerializer(DocumentSerializer):

	user_roles = UserroleSerializer(User_roles, many=True)

	class Meta:
		model = Cells
		depth = 1
		fields = ('id', 'name', 'street', 'street_number', 'user_roles', 'origin')
