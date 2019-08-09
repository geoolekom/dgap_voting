from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from profiles.models import StudentInfo
from social_django.middleware import SocialAuthExceptionMiddleware
from social_core.exceptions import AuthForbidden
from social_core.exceptions import AuthAlreadyAssociated
from social_core.backends.oauth import BaseOAuth2


def set_middlename(backend, user, response, *args, **kwargs):
    """Legacy social auth middleware to set middlename. Currently middlename is stored in :class:`profiles.models.StudentInfo`"""
    if user.userprofile.student_info:
        name = user.userprofile.student_info.fio.split()
        if len(name) == 3:
            user.userprofile.middlename = name[2]
            user.userprofile.save()
    elif backend.name == 'google-oauth2':
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


def approve_student(backend, user, response, *args, **kwargs):
    """Tries to verify user as enrolled student.

    * If backend is ``google-oauth2``, then ``user.email`` should be student's corporate email
    * If backend is ``vk-oauth-2``, then ``user.username`` is vk profile's screen name

    Function is invoked as part of :const:`core.settings.SOCIAL_AUTH_PIPELINE`.
    ``user.email`` & so on are populated after social login also in that pipeline
    """
    profile = getattr(user, 'userprofile', None)
    if profile:
        if not profile.student_info or not profile.is_approved:
            try:
                if backend.name == 'google-oauth2':
                    student_info = StudentInfo.objects.get(phystech__iexact=user.email)
                elif backend.name == 'vk-oauth2':
                    student_info = StudentInfo.objects.get(vk='https://vk.com/' + user.get_username())
                else:
                    return
                profile.is_approved = True
                profile.student_info = student_info
                profile.group = student_info.group
                profile.save()
                user.first_name = student_info.first_name
                user.last_name = student_info.last_name
                user.save()
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                profile.is_approved = False
                profile.save()


class SocialAuthExceptionMiddlewareExtended(SocialAuthExceptionMiddleware):
    """Exception wich raised after authentification error. Describing message is provided

    Currently handled errors:
    ``AuthForbidden``: users can login only with google accounta at @phystech.edu. See :const:`core.settings.SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS`
    ``AuthAlreadyAssociated``: you can associate your social account with only on user.
    """
    def get_message(self, request, exception):
        if type(exception) is AuthForbidden:
            return "Поддерживаются только аккаунты phystech.edu"
        elif type(exception) is AuthAlreadyAssociated:
            return "Данный аккаунт phystech.edu или Вконтакте уже привязан"
        else:
            return str(exception)


class MiptOAuth2(BaseOAuth2):
    """MIPT OAuth authentication backend. Not used currently"""
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
