from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, is_active, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан.')

        if 'username' in extra_fields:
            del extra_fields['username']

        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser,
                          is_active=is_active, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, is_active=True, **extra_fields):
        return self._create_user(email, password, False, False, is_active, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True, **extra_fields)