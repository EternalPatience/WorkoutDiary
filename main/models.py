from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True,
                                       db_index=True,
                                       verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(
        default=True, verbose_name='Слать оповещения о новых комментариях?')


    def delete(self, *args, **kwargs):
        for workout in self.workout_set.all():
            workout.delete()
        super().delete(*args, **kwargs)


    class Meta(AbstractUser.Meta):
        pass


class Workout(models.Model):
    """"Workout description"""
    sportsman_name = models.CharField(max_length=50, verbose_name='Имя спортсмена')
    
    name = models.CharField(max_length=150, verbose_name='Название')
    created_at = models.DateTimeField(auto_now=False,
                                      verbose_name='Дата тренировки',
                                      db_index=True,
                                      editable=True)
    comment = models.TextField(null=True,
                               blank=True,
                               verbose_name='Комментарий')

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"

    def __str__(self):
        return self.name


class Exercise(models.Model):
    """Exercise model that is connected to workout model"""
    workout = models.ForeignKey(Workout,
                                on_delete=models.PROTECT,
                                verbose_name="Тренировка")
    name = models.CharField(max_length=150, verbose_name='Название')

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"

    def __str__(self):
        return self.name


class SetDescription(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT, verbose_name="Упражнение")
    number = models.PositiveSmallIntegerField(verbose_name='№ подхода')
    weight = models.FloatField(verbose_name='Вес')
    repeats = models.PositiveSmallIntegerField(default=0,
                                               verbose_name='Повторения')

    class Meta:
        verbose_name = 'Описание подхода'
        verbose_name_plural = 'Описание подходов'
        ordering = ['number']

    def __str__(self):
        return ('Подход № ' + str(self.number) +" " + str(self.exercise))