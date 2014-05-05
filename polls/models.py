from django.db import models

class Poll(models.Model):
    name = models.CharField('Название опроса', max_length=50)
    question = models.CharField('Вопрос', max_length=200)
    begin_date = models.DateTimeField('Начало голосования')
    end_date = models.DateTimeField('Конец голосования')
    target_room = models.CharField('Целевая комната', max_length=10) #предполагается использование регулярных выражений
    target_group = models.CharField('Целевая группа', max_length=10) #TODO значения по умолчанию для target, покрывающие все комнаты/группы
    public = models.BooleanField('Открытое голосование', default = True)
    ONE = 'ONE'
    MANY = 'MANY'
    OWN = 'OWN'
    ANSWER_TYPE_CHOICES = (
        (ONE , 'Выбор одного варианта'),
        (MANY , 'Выбор нескольких вариантов'),
        (OWN , 'Свой вариант'),
    )
    answer_type = models.CharField(max_length=10, choices = ANSWER_TYPE_CHOICES, default = ONE)


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

