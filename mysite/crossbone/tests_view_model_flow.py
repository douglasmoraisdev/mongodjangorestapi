import test_addons
from crossbone.models import *
from django.test import TestCase
from django.test import Client
from bson.objectid import ObjectId

client = Client()


class ViewModelTest_Add(test_addons.MongoTestCase):

	def test_add_user(self):

		response = client.post('/crossbone/novouser', {'nome_usuario':'TioJoao'})

		self.assertEquals(Users.objects[0].name, 'TioJoao')


	def test_add_role(self):

		response = client.post('/crossbone/novorole', {'nome_funcao':'Lider'})

		self.assertEquals(Roles.objects[0].name, 'Lider')


	def test_add_grouptype(self):

		response = client.post('/crossbone/novogrouptype', {'codigo_tipo_grupo':'celula', 'nome_tipo_grupo':'Célula'})

		self.assertEquals(Groups_types.objects[0].code, 'celula')
		self.assertEquals(Groups_types.objects[0].name, 'Célula')		


	def test_add_newevent(self):

		#group = Groups()
		users = Users()
		roles = Roles()

		users.add_user('Joao')
		users.add_user('Pedro')

		roles.add_role('Lider')
		roles.add_role('Membro')

		users1_id = ObjectId(Users.objects[0].id)
		users2_id = ObjectId(Users.objects[1].id)

		roles1_id = ObjectId(Roles.objects[0].id)
		roles2_id = ObjectId(Roles.objects[1].id)

		host = ''
		event_roles = []
		event_roles.append({'user_group123': users1_id})
		event_roles.append({'user_group456': users2_id})
		event_roles.append({'user_roles123-multiple': roles1_id})
		event_roles.append({'user_roles456-multiple': roles2_id})		
		some_data = 'Reuniao de celula'

		response = client.post('/crossbone/newevent', 
									{
										'grupo-origem-evento': host,
										'user-groupcf3b6b08': users1_id,
										'user-groupd2d32710': users2_id,
										'user-rolecf3b6b08-multiple': [roles1_id],
										'user-roled2d32710-multiple': [roles2_id],
										'nome-grupo-evento':some_data, 										
									}
								)		
		#newevent POST example
		#grupo-origem-evento:57ffea0b6096c85ebb6cae6e
		#nome-grupo-evento:Reuniao de Celula
		#user-groupcf3b6b08-9239-11e6-917e-782bcbed44aa:58011fd66096c87b3b3e907f
		#user-rolecf3b6b08-9239-11e6-917e-782bcbed44aa-multiple:580120046096c87b3b3e9082
		#user-groupd2d32710-9239-11e6-917e-782bcbed44aa:58011fdd6096c87b3b3e9080
		#user-roled2d32710-9239-11e6-917e-782bcbed44aa-multiple:5801200b6096c87b3b3e9083
		#user-roled2d32710-9239-11e6-917e-782bcbed44aa-multiple:580120126096c87b3b3e9084		

		self.assertEquals(Events.objects[0].host, host or None)
		self.assertIn(ObjectId(Events.objects[0].event_roles[0].user.id), [users1_id,users2_id])
		self.assertIn(ObjectId(Events.objects[0].event_roles[1].user.id), [users1_id,users2_id])
		self.assertIn(ObjectId(Events.objects[0].event_roles[0].role.id), [roles1_id,roles2_id])
		self.assertIn(ObjectId(Events.objects[0].event_roles[1].role.id), [roles1_id,roles2_id])		
		self.assertEquals(Events.objects[0].data['name'], some_data)		