from crossbone.models import *

import test_addons



class ModelsTest_Group(test_addons.MongoTestCase):

	def test_dict_deep_group(self):

		Groups.objects.create(
			group_type=['Celula'],
			origin='',
			groups_over=[],
			groups_under=[],
			user_roles = [],			
			data={'name':
						{	'first_name':'Joao',
							'last_name':'Silva'
						}
				}
		)

		self.assertEquals(Groups.objects[0].data['name']['last_name'], 'Silva')


class ModelsTest_Users(test_addons.MongoTestCase):

	def test_dict_deep_user(self):

		Users.objects.create(
			name='Joao',	
			data={'name':
						{	'first_name':'Joao',
							'last_name':'Silva'
						}
				}
		)

		self.assertEquals(Users.objects[0].data['name']['last_name'], 'Silva')
