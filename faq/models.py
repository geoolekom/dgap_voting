from django.db import models
from django_bleach.models import BleachField

# Create your models here.
class QA(models.Model):
    VOTING = 'VOTING'
    ORGANAZIER = 'ORGANAZIER'
    AUDIENCE_CHOICES = (
        (VOTING, 'Голосующему'),
        (ORGANAZIER, 'Организатору голосования'),
    )
    audience = models.CharField(max_length=30, choices=AUDIENCE_CHOICES,
                                default=VOTING)
    question = models.CharField(max_length=800)
    answer = BleachField(max_length=800)

    def __str__(self):
        for item in self.AUDIENCE_CHOICES:
            if item[0] == self.audience:
                return item[1] + ': ' + self.question

    class Meta:
        verbose_name = 'Question/Answer'
        verbose_name_plural = 'FAQ'
