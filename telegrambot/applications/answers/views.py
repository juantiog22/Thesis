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
    answers = Answer.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=answers_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Question', 'Response', 'Suscriber', 'Date'])
    answer_fields = answers.values_list('question__title', 'response', 'suscriber__username', 'date')
    for answer in answer_fields:
        writer.writerow(answer)
    return response