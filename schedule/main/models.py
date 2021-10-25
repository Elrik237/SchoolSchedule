from django.db import models

class Teachers (models.Model):

    fio = models.CharField("ФИО преподавателя" ,max_length=150)

    class Meta:
        verbose_name = 'Список преподавателей'
        verbose_name_plural = 'Список преподавателей'

    def __str__(self):
        return self.fio

class Groups (models.Model):

    name = models.CharField("Класса" ,max_length=3)

    class Meta:
        verbose_name = 'Список классов'
        verbose_name_plural = 'Список классов'

    def __str__(self):
        return self.name

class Schedule (models.Model):

    day = models.DateField("Дата" ,max_length=150)
    time = models.CharField("Время" ,max_length=150)
    discipline = models.CharField("Дисциплина" ,max_length=250)
    teacher  = models.CharField("ФИО преподавателя" ,max_length=150)
    group  = models.ForeignKey(Groups, on_delete=models.CASCADE,)
    place = models.ForeignKey(Teachers, on_delete=models.CASCADE,)

    class Meta:
        verbose_name = 'Рассписание уроков'
        verbose_name_plural = 'Рассписание уроков'

    def __str__(self):
        return "Schedule"