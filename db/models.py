import uuid 
from django.db import models


class Constraint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Описание')

    class Meta:
        abstract = True


class ISSModuleConstraint(Constraint):
    class Meta:
        verbose_name = 'Ограничение по модулю МКС'
        verbose_name_plural = 'Ограничения по модулю МКС'


class TechnicalConstraint(Constraint):
    class Meta:
        verbose_name = 'Техническое ограничение смежных инструкций'
        verbose_name_plural = 'Технические ограничения смежных инструкций'


class MoralConstraint(Constraint):
    class Meta:
        verbose_name = 'Моральное ограничение смежных инструкций'
        verbose_name_plural = 'Моральные ограничения смежных инструкций'


class OtherConstraint(Constraint):
    class Meta:
        verbose_name = 'Иное ограничение смежных инструкций'
        verbose_name_plural = 'Иные ограничения смежных инструкций'


class Instruction(models.Model):
    class PriorityChoices(models.TextChoices):
        VERY_HIGH = 'very_high','Очень высокий'
        HIGH = 'high','Высокий'
        MEDIUM = 'medium', 'Средний'
        LOW = 'low','Низкий'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Описание')
    minimum_execution_time = models.DurationField('Минимальное время выполнения')
    iss_module_constraint = models.ManyToManyField(ISSModuleConstraint)
    technical_constraint = models.ManyToManyField(TechnicalConstraint)
    moral_constraint = models.ManyToManyField(MoralConstraint)
    other_constraint = models.ManyToManyField(OtherConstraint)
    priority = models.CharField('Приоритет', max_length=255, choices=PriorityChoices.choices, default=None)

    class Meta:
        verbose_name = 'Инструкция'
        verbose_name_plural = 'Инструкции'


class Plan(models.Model):
    class TypeChoices(models.TextChoices):
        DAY = 'day','Дневной'
        WEEK = 'week','Недельный'
        MONTH = 'month','Месячный'
        YEAR = 'year','Годовой'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self', verbose_name='Входит в план', on_delete=models.CASCADE)
    approved = models.BooleanField('Согласовано', default=False)
    type = models.CharField('Тип', max_length=255, choices=TypeChoices.choices, default=None)
    instructions = models.ManyToManyField(Instruction, verbose_name='Инструкции')

    class Meta:
        verbose_name = 'План полета'
        verbose_name_plural = 'Планы полета'
