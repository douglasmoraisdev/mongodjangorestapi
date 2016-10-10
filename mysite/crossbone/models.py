from django.db import models
from mongoengine import *
# Create your models here.


class Groups(Document):
	email = StringField(required=True)
	tipo = StringField(max_length=50)
	name = StringField(max_length=50)

class Users(Document):
	email = StringField(required=True)
	name = StringField(max_length=50)	



class Events(Document):
	email = StringField(required=True)



class Roles(Document):
	email = StringField(required=True)
