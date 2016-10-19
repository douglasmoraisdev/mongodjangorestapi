from django.db import models
from mongoengine import *
from crossbone.models.roles import *

# Create your models here.

class Users(Document):
	name = StringField(max_length=50)
	auth = StringField(max_length=255)
	extra_data = DictField()

	def add_user(self, user_name, extra_data=None):


		ex_data = dict()

		if extra_data:

			#empty 
			extra_data['first_name'] = extra_data['first_name'] if ('first_name' in extra_data) else ''
			extra_data['secound_name'] = extra_data['secound_name'] if ('secound_name' in extra_data) else ''
			extra_data['email'] = extra_data['email'] if ('email' in extra_data) else ''
			extra_data['birthday_date'] = extra_data['birthday_date'] if ('birthday_date' in extra_data) else ''
			extra_data['address'] = extra_data['address'] if ('address' in extra_data) else ''
			extra_data['city'] = extra_data['city'] if ('city' in extra_data) else ''
			extra_data['state'] = extra_data['state'] if ('state' in extra_data) else ''
			extra_data['country'] = extra_data['country'] if ('country' in extra_data) else ''
			extra_data['zipcode'] = extra_data['zipcode'] if ('zipcode' in extra_data) else ''

			ex_data = dict(
				{'first_name':
					{'name':'Primeiro Nome','value': extra_data['first_name']},
			 	 'secound_name':
					{'name':'Sobrenome','value': extra_data['secound_name']},
				 'email':
					{'name':'Email','value': extra_data['email']},
				 'birthday_date':
					{'name':'Nascimento','value': extra_data['birthday_date']},
				 'address':
					{'name':'Endereço','value': extra_data['address']},
				 'city':
					{'name':'Cidade','value': extra_data['city']},
				 'state':
					{'name':'Estado','value': extra_data['state']},
				 'country':
					{'name':'País','value': extra_data['country']},
				 'zipcode':
					{'name':'Cep','value': extra_data['zipcode']},
				}
			)		

		Users.objects.create(
			name = user_name,
			extra_data = ex_data
			)

class User_roles(EmbeddedDocument):
	user = ReferenceField(Users)
	role = ReferenceField(Roles)		