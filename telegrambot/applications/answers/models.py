from django.db import models
from django.utils import timezone

from applications.questions.models import Question, PosibleAnswers, QuestionBlock
#from applications.suscribers.models import Suscriber
from applications.usuarios.models import Suscriber


class Answer(models.Model):
    response = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    suscriber = models.ForeignKey(Suscriber, related_name='suscribers', on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now, blank=True)
    block = models.ForeignKey(QuestionBlock, related_name='answer_block', on_delete=models.CASCADE, blank=True, null=True)

    
    def get_date(self):
        return self.date
    
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


    