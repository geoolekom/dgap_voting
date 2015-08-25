from django.template import RequestContext, loader
from polls.models import Poll 
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from sendfile import sendfile
import os.path
from django.conf import settings
import subprocess
from django_bleach.models import BleachField
import pyqrcode
from django.core.management import call_command
import logging

logger = logging.getLogger('django.request')

def make_html_advert(request, poll_id, poll_obj):
    qrcode_addr = os.path.join(settings.SENDFILE_ROOT, "qrcode{}.png".format(poll_id))
    
    try:
        qr = pyqrcode.create(request.build_absolute_uri(reverse('polls:detail', args=[poll_id,])))
        qr.png(qrcode_addr, scale=6)
    except Exception as e:
        logger.warning(e)
    
    return loader.render_to_string('polls/advert.html', {
        'poll_obj': poll_obj,
        'filename': 'adv_html',
        'main_text': request.POST['main_text'],
        'author_name': request.POST['author_name'],
        'poll_address': request.build_absolute_uri(reverse('polls:detail', args=[poll_id,])),
        'site_name': request.get_host(),
        'qrcode_addr': qrcode_addr
    }, RequestContext(request))

def create_advert(request, poll_id):
    poll_obj = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/create_advert.html', {
        'poll_id': poll_id,
        'allowed_tags': settings.BLEACH_ALLOWED_TAGS,
        'allowed_attrs': settings.BLEACH_ALLOWED_ATTRIBUTES,
        'allowed_styles': settings.BLEACH_ALLOWED_STYLES
    })

def html_to_pdf(html_filename, pdf_filename):
    error = subprocess.call(["wkhtmltopdf", "--minimum-font-size", "18", "--margin-top", "25mm", "--margin-bottom", "25mm", "--margin-left", "20mm", "--margin-right", "20mm", html_filename, pdf_filename])
    return not error  

def make_pdf(request, poll_id):
    try:
        poll_obj = get_object_or_404(Poll, pk=poll_id)
        filename = os.path.join(settings.SENDFILE_ROOT, "poll{}".format(poll_id)) 
        html_filename = "{}.html".format(filename)
        pdf_filename = "{}.pdf".format(filename)
        
        with open(html_filename, 'w') as htmlfile:
            htmlfile.write(make_html_advert(request, poll_id, poll_obj))
        
        if not html_to_pdf(html_filename, pdf_filename):
            raise Exception("Something is wrong with wkhtmltopdf, see logs to understand")
        return sendfile(request, pdf_filename, attachment=True, attachment_filename="{}.pdf".format(poll_obj.name))
    except Exception as e: 
        logger.warning(e)
        message = "Невозможно сгенерировать объявление. При повторном возникновении проблемы обратитесь к администратору."
    messages.warning(request, message)
    return redirect('polls:done')


