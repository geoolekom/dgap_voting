"""
Here are some functions I need working with python-social-auth
"""

def cut_firstname(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        user.first_name = user.first_name.split()[0]
        user.save()



from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social.exceptions import AuthForbidden
from social.exceptions import AuthAlreadyAssociated

class SocialAuthExceptionMiddlewareExtended(SocialAuthExceptionMiddleware):
    def get_message(self, request, exception):
        if type(exception) is AuthForbidden:
            return "Поддерживаются только аккаунты phystech.edu"
        elif type(exception) is AuthAlreadyAssociated:
            return "Данный аккаунт phystech.edu уже привязан"
        else:
            return str(exception)




from social.backends.oauth import BaseOAuth2

class MiptOAuth2(BaseOAuth2):
    """MIPT OAuth authentication backend"""
    name = 'mipt-oauth2'
    ID_KEY = 'id'
    AUTHORIZATION_URL = 'https://mipt.ru/oauth/authorize.php'
    ACCESS_TOKEN_URL = 'https://mipt.ru/oauth/token.php'
    ACCESS_TOKEN_METHOD = 'POST'
    DEFAULT_SCOPE = ['userinfo', 'settle', 'email']
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires_in', 'expires_in'),
        ('refresh_token', 'refresh_token', True),
        ('token_type', 'token_type'),
    ]

    def get_user_details(self, response):
        return {'username': response.get('login'),
                'email': response.get('email') or '',
                'first_name': response.get('first_name'),
                'last_name': response.get('last_name'),
                'middle_name': response.get('second_name'),
                }

    def user_data(self, access_token, *args, **kwargs):
        response = self.get_json('http://mipt.ru/oauth/api.php',
                params={'access_token': access_token, 'get': 'settle'})
        response = self.request('http://mipt.ru/oauth/api.php',
                params={'access_token': access_token, 'get': 'settle'})
        print(response)
        response = self.get_json('http://mipt.ru/oauth/api.php',
                params={'access_token': access_token, 'get': 'userinfo'})
        #print(response)
        return response
