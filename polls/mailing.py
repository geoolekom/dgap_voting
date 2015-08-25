from polls.models import Poll, UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.management import call_command
from django.contrib.auth.decorators import login_required, user_passes_test

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def approve_mailing(request, poll_id):    
    poll_obj = get_object_or_404(Poll, pk=poll_id)
    recipients = [profile.user for profile in UserProfile.objects.filter(is_subscribed=True) if profile.is_approved() and poll_obj.is_user_target(profile.user) and not poll_obj.is_user_voted(profile.user)]
    
    return render(request, 'polls/mailing_confirm.html', {
        'poll_id': poll_id,
        'poll': poll_obj,
        'addr_num': len(recipients)
    })


@login_required
@user_passes_test(is_staff)
def mail_unvoted(request, poll_id):    
    poll_obj = get_object_or_404(Poll, pk=poll_id)
    
    call_command('mailing_unvoted', poll_id)
    
    poll_obj.last_mailing = timezone.now()
    poll_obj.times_mailed += 1
    poll_obj.save()
    
    message = "Рассылка успешно произведена"
    messages.info(request, message)
    return redirect('admin:polls_poll_changelist')


