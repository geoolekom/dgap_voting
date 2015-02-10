"""
Here are some functions I need working with python-social-auth
"""

def cut_firstname(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        user.first_name = user.first_name.split()[0]
        user.save()



from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social.exceptions import AuthForbidden

class SocialAuthExceptionMiddlewareExtended(SocialAuthExceptionMiddleware):
    def get_message(self, request, exception):
        if type(exception) is AuthForbidden:
            return "Поддерживаются только аккаунты phystech.edu"
        else:
            return str(exception)

