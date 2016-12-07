from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from bethelgroups.models import *


def bethel_auth_required(func=None):
    '''
	@bethel_auth_required - decorator
        Verify the login status of user
        if not logged in then redirect to login page configured on settings.LOGIN_URL
	return a list of user_apps with objects and permissions
    '''

    def _decorated(request, *args, **kwargs):

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
					'events_perm' events_perms,
					'groups_obj': user_groups,
					'groups_perm': groups_perms
				  }

            return func(request, *args, **kwargs)

    return _decorated



def bethel_login_required2(func=None, home_url=None, redirect_field_name=None):

    def _decorated(request, *args, **kwargs):
        print("dlaaaee")
        return HttpResponse('dale')
        #return func(request, *args, **kwargs)

    return _decorated
