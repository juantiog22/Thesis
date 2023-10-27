from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.generic import (
    ListView,
)

from .models import Answer
from applications.usuarios.models import Suscriber

import csv
import io
from django.utils.encoding import smart_str


class AnswersListView(LoginRequiredMixin, ListView):
    template_name = 'answers/list_answers.html'
    paginate_by = 20
    model = Answer
    context_object_name = 'lista_answers'
    login_url = reverse_lazy('usuarios_app:user-login')

    
    def get_queryset(self, *args, **kwargs):
        lista_answers = super(AnswersListView, self).get_queryset(*args, **kwargs)
        lista_answers = lista_answers.order_by("-id")
        return lista_answers



def export_to_csv(request):
    answers = Answer.objects.all().order_by('-date')
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=';')

    writer.writerow([smart_str('Block'), smart_str('Question'), smart_str('Response'), smart_str('Subscriber'), smart_str('Date')])
    
    for answer in answers:
        block = smart_str(answer.block.block)
        question = smart_str(answer.question.title)
        response = smart_str(answer.response)
        subscriber_username = smart_str(answer.suscriber.username)
        date = smart_str(answer.date.strftime('%Y-%m-%d'))

        writer.writerow([block, question, response, subscriber_username, date])
    
    csv_file_name = 'answers_export.csv'
    with open(csv_file_name, 'w', encoding='latin1') as csv_file:
        csv_file.write(buffer.getvalue())
    
    with open(csv_file_name, 'rb') as csv_file:
        response = HttpResponse(csv_file.read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={csv_file_name}'
    
    return response