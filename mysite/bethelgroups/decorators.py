from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect


def bethel_login_required(func=None, home_url=None, redirect_field_name=None):
    '''
        Verify the login status of user
        if not logged in then redirect to login page configured on settings.LOGIN_URL
    '''

    def _decorated(request, *args, **kwargs):

        if (('user_id' not in request.session) or (request.session['user_id'] == '')):
            return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            return func(request, *args, **kwargs)

    return _decorated



def bethel_login_required2(func=None, home_url=None, redirect_field_name=None):

    def _decorated(request, *args, **kwargs):
        print("dlaaaee")
        return HttpResponse('dale')
        #return func(request, *args, **kwargs)

    return _decorated    