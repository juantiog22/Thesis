from django.db import models

    

class Context(models.Model):

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Context'
        verbose_name_plural = 'Contexts'

    
    def __str__(self):
        return self.name

    def name_display(self):
        return self.name


class Message(models.Model):

    text = models.CharField(max_length=300)
    context = models.ForeignKey(Context, related_name='messages', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.text