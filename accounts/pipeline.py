from social_core.backends.google import GoogleOAuth2


def populate_user(backend, user, *args, **kwargs):
    if backend.name == GoogleOAuth2.name:
        user.is_verified = True

        google_first_name = user.first_name
        name_parts = google_first_name.split(' ')
        if len(name_parts) == 2:
            user.first_name = name_parts[0]
            user.patronymic = name_parts[1]

        user.save()
    return {
        'user': user
    }
