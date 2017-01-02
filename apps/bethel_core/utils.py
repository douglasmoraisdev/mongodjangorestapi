'''
	Common util bethel_core functions
'''
from django.conf import settings
import logging
from bethel_core.models import *
from bson.objectid import ObjectId

import googlemaps

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
					if (usersA.user.geolocation['coordinates'] == usersB.user.geolocation['coordinates']):

						tested_user_id.append(usersA.user.id)
						tested_user_id.append(usersB.user.id)

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

def parse_users_multi_role(usersObj, rolesObj):

	user_added = usersObj
	roles_added = rolesObj

	roles_obj = []
	servant_roles = []


	#servants added get list
	for key, users in enumerate(user_added):
		user_obj =	Users.objects.get(id=ObjectId(users))

		for roles in roles_added[key].split(","):

			roles_add = Roles.objects.get(id=ObjectId(roles))
			roles_obj.append(roles_add)

		servant_roles.append(User_roles(user=user_obj, role=roles_obj))

		roles_obj = []

	return servant_roles

def parse_users_fixed_role(usersObj, roleCode):

	member_added = usersObj

	member_role_code = []
	members_roles = []

	member_role_code = Roles.objects.get(code=roleCode)
	for key, users in enumerate(member_added):
		user_obj =	Users.objects.get(id=ObjectId(users))

		members_roles.append(User_roles(user=user_obj, role=[member_role_code]))

	return members_roles	

def generate_geolocation(address):

	default_no_found = (-30.1169633,-51.3392944)

	geocode_result = []

	# Google Maps Client
	gmaps = googlemaps.Client(key='AIzaSyD1FfhbFJv88cNCVu5xcHBt0rw4eeJYQOk')

	if address.strip() != '':
		#geocode_result = gmaps.geocode(address=address , region='br')

		if geocode_result == []:
			geocode_result = default_no_found

	else:
		geocode_result = default_no_found

	if geocode_result == default_no_found:
		return geocode_result
	else:
		return (geocode_result[0]['geometry']['location']['lat'] , geocode_result[0]['geometry']['location']['lng'])
