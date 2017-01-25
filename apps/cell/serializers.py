from .models import Cells

from user.models import BUser_roles
from user.serializers import UserroleSerializer

from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
from rest_framework.serializers import SerializerMethodField

class CellSerializer(DocumentSerializer):

	user_roles = UserroleSerializer(BUser_roles, many=True)
	members_count = SerializerMethodField()
	members_geolocation = SerializerMethodField()


	class Meta:
		model = Cells
		depth = 2
		fields = ('id', 'name', 'user_roles', 'members_count', 'members_geolocation')


	def get_members_count(self, obj):
		return obj.user_roles.count()


	def get_members_geolocation(self, obj):


		member_maps = []
		maps_dict	= dict()		

		grouped_coordinates = []
		grouped_dict = dict()

		user_info_dict = dict()

		gen_coordinates_ids = []
		for us in obj.user_roles:

			latlang = str(us.user.geolocation['coordinates'])

			maps_dict = {latlang : [us]}

			member_maps.append(maps_dict)

			gen_coordinates_ids.append(latlang)	

		#disctict ids
		gen_coordinates_ids = list(set(gen_coordinates_ids))
		
		for item in gen_coordinates_ids:
			grouped_dict = {item : []}

			for value in member_maps:
				if list(value)[0] == item:

					user_info_dict = {
						'id' : str(value[item][0].user.id),
						'first_name' : value[item][0].user.first_name,
						'last_name' : value[item][0].user.last_name,
					}

					grouped_dict[item].append(user_info_dict)
		
			grouped_coordinates.append(grouped_dict)


		return grouped_coordinates
