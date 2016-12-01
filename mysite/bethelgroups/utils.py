'''
	Common util bethelgroups functions
'''
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def get_users_geo(usersObj):
	'''
		Parse a user_object in a list of agrouped address for google maps
		if 2 ou more users have the same address they are agrouped
	'''

	users = usersObj
	member_maps	 = []

	tested_user_id = []
	for usersA in users:

		#Verify same address users
		for usersB in users:

			if (usersA.user.id != usersB.user.id):
				if (usersB.user.id not in tested_user_id):				
					if (usersA.user.extra_data['addr_lat'] == usersB.user.extra_data['addr_lat']) and (usersA.user.extra_data['addr_lng'] == usersB.user.extra_data['addr_lng']):

						tested_user_id.append(usersA.user.id)
						tested_user_id.append(usersB.user.id)
						logger.error('Mesmo endereço: %s e %s' % (usersA.user.extra_data['first_name'], usersB.user.extra_data['first_name']))

						addr_maps_info = {
							'users' : [usersA, usersB]
						}

						member_maps.append(addr_maps_info)

		#Add other members no duplied
		if (usersA.user.id not in tested_user_id):

			addr_maps_info = {
				'users' : [usersA]
			}

			member_maps.append(addr_maps_info)

	return member_maps