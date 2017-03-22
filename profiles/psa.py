"""
Here are some functions I need working with python-social-auth
"""
from profiles.models import UserInformation


def set_middlename(backend, user, response, *args, **kwargs):
    # print(response)
    if backend.name == 'google-oauth2':
        name = user.first_name.split()
        if len(name) == 2:
            user.first_name, user.userprofile.middlename = name
            user.save()
            user.userprofile.save()
        elif len(name) == 1:
            user.userprofile.middlename = ''
            user.userprofile.save()
    elif backend.name == 'mipt-oauth2':
        user.userprofile.middlename = response['secondname']
        user.userprofile.save()

    if backend.name == 'google-oauth2':
        user_informations = UserInformation.objects.filter(phystech__iexact=user.email)
        if len(user_informations) == 1:
            user.userprofile.is_approved = True
            user.userprofile.user_information = user_informations[0]
            user.userprofile.group = user_informations[0].group
            user.userprofile.save()
        elif len(user_informations) < 1:
            user.userprofile.is_approved = False
            user.userprofile.save()
        else:
            user.userprofile.is_approved = False
            user.userprofile.save()
    elif backend.name == 'vk-oauth2':
        user_informations = UserInformation.objects.filter(vk='https://vk.com/' + user.username)
        if len(user_informations) == 1:
            user.userprofile.is_approved = True
            user.userprofile.user_information = user_informations[0]
            user.userprofile.group = user_informations[0].group
            user.userprofile.save()
        elif len(user_informations) < 1:
            user.userprofile.is_approved = False
            user.userprofile.save()
        else:
            user.userprofile.is_approved = False
            user.userprofile.save()



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
    API_URL = 'https://mipt.ru/oauth/api.php'
    ACCESS_TOKEN_METHOD = 'POST'
    DEFAULT_SCOPE = ['userinfo', 'settle', 'email']
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires_in', 'expires_in'),
        ('refresh_token', 'refresh_token', True),
        ('token_type', 'token_type'),
        ('login', 'login'),
    ]

    def get_user_details(self, response):
        return {'username': response.get('login'),
                'email': response.get('email') or '',
                'first_name': response.get('firstname'),
                'last_name': response.get('lastname'),
                }

    def user_data(self, access_token, *args, **kwargs):
        userinfo = self.get_json(
            self.API_URL,
            params={'access_token': access_token, 'get': 'userinfo'}
        )
        # print(userinfo)
        email = self.get_json(
            self.API_URL,
            params={'access_token': access_token, 'get': 'email'}
        )
        # print(email)
        userinfo.update(email)
        response = userinfo
        # print(response)
        return response
