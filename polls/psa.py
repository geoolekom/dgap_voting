"""
Here are some functions I need working with python-social-auth
"""

def cut_firstname(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        user.first_name = user.first_name.split()[0]
        user.save()
