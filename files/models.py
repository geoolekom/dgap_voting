from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.views.generic.edit import ModelFormMixin

from .forms import FilesFormSet

# Create your models here.
class Document(models.Model):
    file = models.FileField("Изображение", upload_to='feedback/')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')
    # is_image = models.BooleanField("Является изображением", default=True)

    class Meta:
        verbose_name = "документ"
        verbose_name_plural = "документы"

    def __str__(self):
        return "Документ {} к событию {}".format(self.file.name, self.object)


class FileUploadMixin(ModelFormMixin):

    def get_context_data(self, **kwargs):
        data = super(FileUploadMixin, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = FilesFormSet(self.request.POST, self.request.FILES)
        else:
            data['formset'] = FilesFormSet()
        return data

    def file_processing(self, content_object):
        for photoform in self.get_context_data()['formset']:
            if photoform.is_valid():
                if photoform.cleaned_data.get('file'):
                    photo = photoform.cleaned_data['file']
                    Document.objects.create(file=photo, object=content_object)
