from crossbone.models import *
from bson.objectid import ObjectId

import test_addons

class ModelsTest_add(test_addons.MongoTestCase):

	def test_add_users(self):

		user = Users()

		user.add_user('Joao')

		self.assertEquals(Users.objects[0].name, 'Joao')	

	def test_add_group_type(self):

		groups_types = Groups_types()

		groups_types.add_group_type('celula', 'Célula', {})

		self.assertEquals(Groups_types.objects[0].code, 'celula')
		self.assertEquals(Groups_types.objects[0].name, 'Célula')

	def test_add_groups(self):

		group = Groups()

		#First Group
		group_type = Groups_types()
		user_roles = []
		data = {'name':'Celula da Alvorada'}
		origin = None
		groups_over = None
		groups_under = None
		user_roles = []

		group_type.add_group_type('celula', 'Célula', {})
		group_type_id = Groups_types.objects[0].id

		group.add_group(group_type_id, origin, groups_over, groups_under, user_roles, {'name':'Celula da Alvorada'})

		self.assertEquals(Groups.objects[0].extra_data['name']['value'], 'Celula da Alvorada')
		self.assertIn(Groups.objects[0].group_type[0].id, [group_type_id])
		self.assertEquals(Groups.objects[0].origin == None, True)
		self.assertEquals(Groups.objects[0].groups_over == [], True)
		self.assertEquals(Groups.objects[0].groups_under == [], True)
		self.assertEquals(Groups.objects[0].user_roles == [], True)

		#Second Group
		user_roles = []
		data = {'name':'Celula Fátima'}
		origin = Groups.objects[0].id
		groups_over = [Groups.objects[0].id]
		groups_under = [Groups.objects[0].id]
		user_roles = []

		group.add_group(group_type_id, origin, groups_over, groups_under, user_roles, {'name':'Celula da Fatima'})

		self.assertEquals(Groups.objects[1].extra_data['name']['value'], 'Celula da Fatima')
		self.assertIn(Groups.objects[1].group_type[0].id, [group_type_id])
		self.assertEquals(Groups.objects[1].origin.id, origin)
		self.assertIn(Groups.objects[1].groups_over[0].id, groups_over)
		self.assertIn(Groups.objects[1].groups_under[0].id, groups_under)
		self.assertEquals(Groups.objects[1].user_roles == [], True)



	def test_add_event(self):

		host = None
		event_roles = []
		some_data = dict()

		event = Events()

		event.add_event(host, event_roles, some_data)

		self.assertEquals(Events.objects[0].host, host)
		self.assertEquals(Events.objects[0].event_roles, event_roles)
		self.assertEquals(Events.objects[0].extra_data, some_data)

	def test_add_roles(self):

		role = Roles()

		role.add_role('Lider')

		self.assertEquals(Roles.objects[0].name, 'Lider')

