from django.db import models
from mongoengine import *

import logging

logger = logging.getLogger(__name__)

class Mig_geostore(Document):
	'''
		Store already searched geocodes from googlemapsapi for re-use 
		and prevent api quotas run out
	'''
	address = StringField(max_length=255)
	lat = StringField(max_length=255)
	lng = StringField(max_length=255)


	meta = { 'indexes' : ['address']}

	def insert_stored_geo(address, lat, lng):

		Mig_geostore.objects.create(
			address = address,
			lat = lat,
			lng = lng
			)


	def get_stored_geo(address):

		try:
			geolocation = Mig_geostore.objects(address=address)

			if (geolocation != None) and (geolocation != []):
				return (geolocation[0].lat, geolocation[0].lng)
			else:
				return False

		except:
			return False

