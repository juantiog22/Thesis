from django.utils import timezone
from django.db import models
from applications.contexts.models import Context
from applications.usuarios.models import User


class Question(models.Model):
    title = models.CharField(max_length=300)
    create = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    
    def __str__(self):
        return self.title 
    
class PosibleAnswers(models.Model):
    texto = models.CharField(max_length=300)
    question = models.ForeignKey(Question, related_name='preguntas', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.texto

class QuestionBlock(models.Model):
    FRECUENCY_CHOICES = (
        ('O', 'Once'),
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
    )

    IMPORTANCE_CHOICES = (
        (1, 'High priority'),
        (2, 'Normal priority'),
        (3, 'Low important'),
    )

    block = models.CharField(max_length=50)
    question = models.ManyToManyField(Question, related_name='blocks')
    context = models.ManyToManyField(Context, related_name='block')
    active = models.BooleanField(default=False)
    frecuency = models.CharField(max_length=1, choices=FRECUENCY_CHOICES, default='O')
    importance = models.IntegerField(choices=IMPORTANCE_CHOICES, default=1)

    class Meta:
        verbose_name = 'Block'
        verbose_name_plural = 'Blocks'

    
    def __str__(self):
        return self.block
    

    

