from django.db import models
from mongoengine import *
# Create your models here.

class Roles(Document):
	name = StringField(max_length=50)
	data = DictField()

class Users(Document):
	name = StringField(max_length=50)
	data = DictField()

class User_roles(EmbeddedDocument):
	user = ReferenceField(Users)
	role = ReferenceField(Roles)

class Groups_types(Document):
	code = StringField(max_length=50)
	name = StringField(max_length=50)

class Groups(Document):
	group_type = ListField(ReferenceField(Groups_types))
	user_roles = EmbeddedDocumentListField(User_roles)
	data = DictField()
	origin = ReferenceField("self", reverse_delete_rule = NULLIFY)
	groups_over = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	groups_under = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))

class Events(Document):
	host = ReferenceField(Groups)
	event_roles = EmbeddedDocumentListField(User_roles)
	data = DictField()
