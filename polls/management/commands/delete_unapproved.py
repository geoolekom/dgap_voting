from django.core.management.base import BaseCommand, CommandError
from polls.models import UserProfile
from django.core.mail import send_mass_mail

class Command(BaseCommand):
    help = 'Deletes unapproved users'

    def handle(self, *args, **options):
        users_to_delete = [profile.user for profile in UserProfile.objects.filter(approval=False)]
        
        datatuple = []
        subject = "Удаление учётной записи на сайте vote.dgap-mipt.ru"
        message = """Здравствуйте, {username}!

Некоторое время назад Вы зарегистрировались в голосовалке ФОПФ (vote.dgap-mipt.ru), но не подтвердили данные профиля. В связи с этим Ваш аккаунт на сайте будет удалён.

Не огорчайтесь! Теперь Вы можете повторно зарегистрироваться по упрощённой форме с использованием своего почтового ящика в домене phystech.edu"""
        from_email = 'vote@dgap.mipt.ru'
        for user in users_to_delete:
            personal_message = message.format(username=user.username)
            datatuple.append((subject, personal_message, from_email, [user.email]))
        send_mass_mail(datatuple)
        
        for user in users_to_delete:
            user.delete()
