from .models import Cells


from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
from rest_framework.serializers import SerializerMethodField

from user.models import BUser_roles
from user.serializers import UserroleSerializer

from cell_metting.models import Cell_mettings

import cell_metting as clm


class CellSerializer(DocumentSerializer):
	'''
		Cell main data
	'''

	user_roles = UserroleSerializer(BUser_roles, many=True, read_only=True)
	members_count = SerializerMethodField(read_only=True)
	members_geolocation = SerializerMethodField(read_only=True)
	mettings = SerializerMethodField(read_only=True)
	

	class Meta:
		model = Cells
		depth = 2
		fields = (  'id', 
					'name', 
					'origin', 
					'user_roles', 
					'members_count', #read_only
					'members_geolocation', #read_only
					
					'zipcode',
					'street',
					'street_number',
					'addr_obs',
					'neigh',
					'city',
					'state',
					
					'mettings' #read_only
				)
				

	def update(self, instance, validated_data):
	    #instance.email = validated_data.get('email', instance.email)
	    instance.name = validated_data.get('name', instance.name)
	    print(validated_data)
	    return instance

	def get_members_count(self, obj):
		return obj.user_roles.count()


	def get_members_geolocation(self, obj):


		member_maps = []
		maps_dict	= dict()		

		celled_coordinates = []
		celled_dict = dict()

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
			celled_dict = {item : []}

			for value in member_maps:
				if list(value)[0] == item:

					user_info_dict = {
						'id' : str(value[item][0].user.id),
						'first_name' : value[item][0].user.first_name,
						'last_name' : value[item][0].user.last_name,
					}

					celled_dict[item].append(user_info_dict)
		
			celled_coordinates.append(celled_dict)


		return celled_coordinates


	def get_mettings(self, obj):
		
		queryset = Cell_mettings.objects(host=str(obj.id))
		serializer = clm.serializers.MettingsofCellSerializer(queryset, many=True)
		return serializer.data



class CellofMettingSerializer(DocumentSerializer):
	'''
		Used to display cells data on a cell_metting
	'''

	user_roles = UserroleSerializer(BUser_roles, many=True, read_only=True)
	mettings = SerializerMethodField(read_only=True)

	class Meta:
		model = Cells
		depth = 2
		fields = (  'id', 
					'name', 
					'user_roles', 
					
					'mettings'
				)

	def get_mettings(self, obj):
		
		queryset = Cell_mettings.objects(host=str(obj.id))
		serializer = clm.serializers.MettingsofCellSerializer(queryset, many=True)
		return serializer.data