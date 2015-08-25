from django.core.management.base import BaseCommand, CommandError
from polls.models import UserProfile, Poll
from django.core.mail import send_mass_mail
from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
import os

def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, connection=None): 
    '''
    Like send_mass_mail, where 'datatuple' after the 'message' contains 'html_message'.
    Providing the ability to send multipart/alternative email as it is possible in
    'send_mail' function.
    '''
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, personal_message, html_personal_message, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, personal_message, from_email, recipient)
        message.attach_alternative(html_personal_message, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)

            
class Command(BaseCommand):
    args = '<poll_id1 poll_id2, ...>'
    help = 'Sends emails to users who haven\'t voted in the poll #poll_id'

    def handle(self, *args, **options):
        for poll_id in args:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "{}" does not exist'.format(poll_id))
            
            site_url = Site.objects.get_current().domain
            if not site_url.startswith('http://'):
                site_url = 'http://%s'%site_url
                
            poll_url = os.path.join(site_url, reverse('polls:detail', args=[poll_id,])[1:])
            unsubscribe_url = os.path.join(site_url, reverse('profiles:profile_view')[1:])                                         
            
            recipients = [profile.user for profile in UserProfile.objects.filter(is_subscribed=True) if profile.is_approved() and poll.is_user_target(profile.user) and not poll.is_user_voted(profile.user)]
            
            subject = 'Вам доступен опрос "{}"'.format(poll.name)
            
            plain_message_template = """Здравствуйте, {username}! 
            
            Приглашаем вас принять участие в опросе «{poll_question}», который доступен вам до {date_to} по адресу {poll_url}. 

            Отписаться от оповещений о новых голосованиях вы можете в личном кабинете пользователя: .
            """
            
            html_message_template = """<p>Здравствуйте, {username}! </p>
            
            <p>Приглашаем вас принять участие в опросе <a href="{poll_url}">«{poll_question}»</a>, который доступен вам до {date_to} на сайте {site_url}.</p>
            
            <p><a href="{poll_url}" style="font-size:large">Голосовать!</a></p><br>
            <hr>
            <a href="{unsubscribe_url}" style="font-size:small">Отписаться</a> от оповещений о новых голосованиях вы можете в личном кабинете пользователя.
            """
            
            datatuple = []
            from_email = 'vote@dgap.mipt.ru'

            for user in recipients:
                name = user.username
                    
                html_message = html_message_template.format(username=name, poll_question=poll.question, date_to=poll.end_date.date(), site_url=site_url, poll_url=poll_url, unsubscribe_url=unsubscribe_url)
                
                plain_message = plain_message_template.format(username=name, poll_url=poll_url, date_to=poll.end_date.date(), poll_question=poll.question)
                
                datatuple.append((subject, plain_message, html_message, from_email, [user.email]))

            send_mass_html_mail(datatuple)
