from django.core.management.base import BaseCommand, CommandError
from polls.models import UserProfile
from django.core.mail import send_mass_mail

class Command(BaseCommand):
    help = 'Sends emails to unapproved users'

    def handle(self, *args, **options):
        recipients = [profile.user for profile in UserProfile.objects.filter(is_approved=False)]
        datatuple = []
        subject = "Проблемы при регистрации"
        message = """Здравствуйте, {username}!

Некоторое время назад Вы зарегистрировались в голосовалке ФОПФ
(vote.dgap-mipt.ru), но не подтвердили данные профиля. Не могли бы Вы
написать, какие возникли проблемы - мы очень хотим их исправить. """
        from_email = 'vote@dgap.mipt.ru'
        for user in recipients:
            personal_message = message.format(username=user.username)
            datatuple.append((subject, personal_message, from_email, [user.email]))
        send_mass_mail(datatuple)
