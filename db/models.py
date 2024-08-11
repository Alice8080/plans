import uuid 
from django.db import models


class Instruction(models.Model):
    """
    Инструкция - это набор действий, которые необходимо выполнить.

    Атрибуты:
        id (UUIDField): Уникальный идентификатор инструкции.
        name (CharField): Название инструкции.
        description (TextField): Описание инструкции.
        minimum_execution_time (DurationField): Минимальное время выполнения инструкции.
        priority (CharField): Приоритет инструкции.
    """
    class PriorityChoices(models.TextChoices):
        VERY_HIGH = 'very_high','Очень высокий'
        HIGH = 'high','Высокий'
        MEDIUM = 'medium', 'Средний'
        LOW = 'low','Низкий'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    minimum_execution_time = models.DurationField('Минимальное время выполнения')
    priority = models.CharField('Приоритет', max_length=255, choices=PriorityChoices.choices, default=None)

    class Meta:
        verbose_name = 'Инструкция'
        verbose_name_plural = 'Инструкции'


class ConstraintType(models.Model):
    """
    Тип ограничения - это категория ограничений, которые могут быть применены к инструкциям.

    Атрибуты:
        id (UUIDField): Уникальный идентификатор типа ограничения.
        name (CharField): Название типа ограничения.
        description (TextField): Описание типа ограничения.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Тип ограничения'
        verbose_name_plural = 'Типы ограничений'


class Constraint(models.Model):
    """
    Ограничение - это конкретное ограничение, которое может быть применено к инструкции.

    Атрибуты:
        id (UUIDField): Уникальный идентификатор ограничения.
        name (CharField): Название ограничения.
        description (TextField): Описание ограничения.
        type (ForeignKey): Тип ограничения.
        instruction (ForeignKey): Инструкция, к которой применено ограничение.
        incompatible_instructions (ManyToManyField): Инструкции, которые несовместимы с этой инструкцией.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    type = models.ForeignKey(ConstraintType, verbose_name='Тип', on_delete=models.SET_NULL, null=True)
    instruction = models.ForeignKey(Instruction, verbose_name='Инструкция', on_delete=models.SET_NULL, null=True)
    incompatible_instructions = models.ManyToManyField(Instruction, verbose_name='Несовместимые с ней инструкции', related_name='incompatible_instructions')

    class Meta:
        verbose_name = 'Ограничение'
        verbose_name_plural = 'Ограничения'


class Plan(models.Model):
    """
    План - это общий план, который может быть использован для организации инструкций.

    Атрибуты:
        id (UUIDField): Уникальный идентификатор плана.
        approved (BooleanField): Признак того, что план одобрен.
    """    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    approved = models.BooleanField('Согласовано', default=False)
    commissioning_date = models.DateField('Дата ввода в действие', null=True, blank=True)

    class Meta:
        abstract = True


class YearPlan(Plan):
    """
    Годовой план полета - это план, который охватывает один год.
    """
    class Meta:
        verbose_name = 'Годовой план полета'
        verbose_name_plural = 'Годовые планы полета'


class MonthPlan(Plan):
    """
    Месячный план полета - это план, который охватывает один месяц.

    Атрибуты:
        year_plan (ForeignKey): Годовой план, в который входит месячный план.
    """
    year_plan = models.ForeignKey(YearPlan, verbose_name='Годовой план', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Месячный план полета'
        verbose_name_plural = 'Месячные планы полета'


class WeekPlan(Plan):
    """
    Недельный план полета - это план, который охватывает одну неделю.

    Атрибуты:
        month_plan (ForeignKey): Месячный план, в который входит недельный план.
    """
    month_plan = models.ForeignKey(MonthPlan, verbose_name='Месячный план', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Недельный план полета'
        verbose_name_plural = 'Недельные планы полета'


class DayPlan(Plan):
    """
    Дневной план полета - это план, который охватывает один день.

    Атрибуты:
        week_plan (ForeignKey): Недельный план, в который входит дневной план.
        instructions (ManyToManyField): Инструкции, которые входят в план.
    """
    week_plan = models.ForeignKey(WeekPlan, verbose_name='Месячный план', on_delete=models.CASCADE)
    instructions = models.ManyToManyField(Instruction, verbose_name='Инструкции', through='DayPlanInstructionInfo')

    class Meta:
        verbose_name = 'Дневной план полета'
        verbose_name_plural = 'Дневные планы полета'


class DayPlanInstructionInfo(models.Model):
    """
    Информация об инструкции дневного плана полета.

    Атрибуты:
        id (UUIDField): Уникальный идентификатор инструкции.
        day_plan (ForeignKey): Дневной план, в который входит инструкция.
        instruction (ForeignKey): Инструкция, которая входит в план.
        number (IntegerField): Номер в последовательности инструкций.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day_plan = models.ForeignKey(DayPlan, verbose_name='Дневной план', on_delete=models.CASCADE)
    instruction = models.ForeignKey(Instruction, verbose_name='Инструкция', on_delete=models.CASCADE)
    number = models.IntegerField('Номер в последовательности инструкций')

    class Meta:
        verbose_name = 'Информация об инструкции дневного плана полета'
        verbose_name_plural = 'Информация об инструкции дневного плана полета'
