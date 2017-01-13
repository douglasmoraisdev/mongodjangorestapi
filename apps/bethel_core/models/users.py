from django.db import models
from mongoengine import *
from bethel_core.models.roles import *
from bethel_core.models.tasks import *

from bethel_core import utils


import logging

logger = logging.getLogger(__name__)

class Users(Document):
	meta = {'allow_inheritance': True}

	mig_id = StringField(max_length=50)

	user_name = StringField(max_length=50)
	auth_type = StringField(max_length=10) #facebook #google #password
	auth_token = StringField(max_length=255) #token or password

	first_name = StringField(max_length=255)
	last_name = StringField(max_length=255)
	cpf = StringField(max_length=11)
	birthday = StringField(max_length=11)

	zipcode = StringField(max_length=255)
	street = StringField(max_length=255)
	street_number = StringField(max_length=255)
	addr_obs = StringField(max_length=255)
	neigh = StringField(max_length=255)
	city = StringField(max_length=255)
	state = StringField(max_length=255)

	profession = StringField(max_length=255)

	extra_data = DictField()

	#internal generated
	geolocation = PointField()

	def add_user(self, mig_id, user_name, auth_type, auth_token, first_name, last_name, cpf, 
		birthday, zipcode, street, street_number, addr_obs, neigh, city, state,
		profession,
		extra_data=None):


		user_geolocation = None

		if street.strip() == '':
			user_geolocation = utils.generate_geolocation("")
		else:
			user_geolocation = utils.generate_geolocation("%s %s, %s, %s, %s" % (street_number, street, neigh, city, state))

		if user_geolocation != None:
			user_geolocation = user_geolocation

		try:
		
			Users.objects.create(
				mig_id = mig_id,
				
				user_name = user_name,
				auth_type = auth_type,
				auth_token = auth_token,

				first_name = first_name,
				last_name = last_name,
				cpf = cpf,
				birthday = birthday,

				zipcode = zipcode,
				street = street,
				street_number = street_number,
				addr_obs = addr_obs,
				neigh = neigh,
				city = city,
				state = state,

				profession = profession,

				extra_data = extra_data,

				geolocation	= user_geolocation
			)

		except Exception as err:
			print("ERRO AO ADICIONAR USUARIO %s" % format(err))


	def get_all(self, search):

		return Users.objects(first_name__icontains=search)


	def get_user_by_id(self, user_id):

		return Users.objects.get(id=user_id)


	def is_auth(self, user_name, auth_token):

		user = Users.objects(user_name=user_name)


		if (user):
			if (user[0].auth_token == auth_token):
				return user[0].id

		return False



class User_roles(EmbeddedDocument):
	user = ReferenceField(Users, dbref=True)
	role = ListField(ReferenceField(Roles, dbref=True))
	task = ListField(ReferenceField(Tasks, dbref=True))
	extra_data = DictField()
