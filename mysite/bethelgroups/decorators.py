from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from bethelgroups.models import *
from django import template
from django.template import loader


def bethel_auth_required(function=None, min_perm=''):
	'''
	@bethel_auth_required - decorator
		Verify the login status of user
		if not logged in then redirect to login page configured on settings.LOGIN_URL
	return a list of user_apps with objects and permissions
	'''


	def _dec(view_func):
		def _view(request, *args, **kwargs):
			
			#Not logged in
			if (('user_id' not in request.session) or (request.session['user_id'] == '')):
				return HttpResponseRedirect(settings.LOGIN_URL)

			else:
				# List user objects agains permissions
				# 'r' = read (min permission)
				# return a kwargs 'user_apps' with a list of app objects
				user_id = request.session['user_id']            
				user_perms = request.session['user_perms']

				user_events = None
				events_perms = ''

				user_groups = None
				groups_perms = ''
				
				if user_perms['events']:
					events_perms = ''.join(user_perms['events']['perm_codes'])
					if ('r' in events_perms):
						user_events = Events().get_user_events_by_type(user_id)


				if user_perms['groups']:
					groups_perms = ''.join(user_perms['groups']['perm_codes'])
					if ('r' in groups_perms):
						user_groups = Groups().get_user_groups_by_type(user_id)

				kwargs['user_apps'] = {
						'events_obj': user_events,
						'events_perm': events_perms,
						'groups_obj': user_groups,
						'groups_perm': groups_perms
					}

				#If min_perm was informed
				if min_perm != '':
					not_autorized = False

					for p in min_perm:

						#groups
						if 'groups' in p:
							if p['groups'] not in groups_perms:
								not_autorized = True

						#events
						if 'events' in p:
							if p['events'] not in events_perms:
								not_autorized = True


					if not_autorized:
						#TODO: a 403 default page template
						#template = loader.get_template(settings.FORBIDDEN_PAGE)
						#return HttpResponseForbidden(template.render(content, template))
						return HttpResponseForbidden('Você não tem autorização para acessar esta página. Contate o administrador do sistema')


			return view_func(request, *args, **kwargs)

		return _view

	if function is None:
		return _dec
	else:
		return _dec(function)
