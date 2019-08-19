from django.db.models import Q
from social_core.backends.google import GoogleOAuth2
from social_core.backends.vk import VKOAuth2

from accounts.models import StudentInfo


def get_student_info(backend, details):
    if backend.name == VKOAuth2.name:
        screen_name = details.get('username')
        query = Q(vk_url='https://vk.com/{0}'.format(screen_name))
    elif backend.name == GoogleOAuth2.name:
        email = details.get('email')
        query = Q(email__iexact=email)
    else:
        return
    return StudentInfo.objects.filter(query).first()


def associate_by_student_info(backend, user, details, **kwargs):
    if user:
        return

    info = get_student_info(backend, details)
    if info:
        return {
            'user': info.user
        }


def student_info_verify(backend, user, details, **kwargs):
    info = get_student_info(backend, details)
    if info and info.user is None:
        fields = ('last_name', 'first_name', 'patronymic', 'group', 'course', 'room', 'sex')
        for field in fields:
            value = getattr(info, field)
            setattr(user, field, value)

        user.is_verified = True
        user.save()

        info.user = user
        info.save()


def phystech_edu_verify(backend, user, details, **kwargs):
    if user.is_verified:
        return
    if backend.name == GoogleOAuth2.name:
        if not user.patronymic:
            google_first_name = details.get('first_name')
            name_parts = google_first_name.split()
            if len(name_parts) == 2:
                user.first_name = name_parts[0]
                user.patronymic = name_parts[1]
        user.is_verified = True
        user.save()
