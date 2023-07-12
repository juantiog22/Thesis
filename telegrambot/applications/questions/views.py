from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, FormMixin, DeletionMixin
from django.core.paginator import Paginator
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    DeleteView,
    UpdateView,
)

from .models import Question, PosibleAnswers, QuestionBlock
from .forms import PreguntaForm, PosibleAnswersFormSet, BlockForm
# Create your views here.

class ListQuestions(LoginRequiredMixin, DeletionMixin, ListView):
    template_name = 'questions/list_questions.html'
    paginate_by = 10
    model = Question
    context_object_name = 'lista_questions'
    login_url = reverse_lazy('usuarios_app:user-login')

    def get_queryset(self, *args, **kwargs):
        lista_questions = super(ListQuestions, self).get_queryset(*args, **kwargs)
        lista_questions = lista_questions.order_by("-create")
        return lista_questions
    

class ListarRespuestas(DetailView):
    template_name = 'questions/list_answers.html'
    model = Question
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


    

class NewQuestionView(LoginRequiredMixin, FormView):
    template_name = 'questions/add_question.html'
    form_class = PreguntaForm
    login_url = reverse_lazy('usuarios_app:user-login')

    def get_success_url(self):
        return reverse_lazy('questions_app:questions_all')

    def get_queryset(self):
        pregunta = self.kwargs['texto']
        lista = PosibleAnswers.objects.filter(
            question__title=pregunta
        )
        return lista
    
    def form_valid(self, form):
        titulo = form.cleaned_data['titulo']
        responses = form.cleaned_data['responses_field']
        quest=Question.objects.create(
            title=titulo 
        )
        for response in responses:
            PosibleAnswers.objects.create(
                texto=response,
                question=quest
            )
            
        return super(NewQuestionView, self).form_valid(form)
    


class QuestionUpdateView(LoginRequiredMixin, FormMixin, DetailView):
     template_name = 'questions/update_question.html'
     form_class = PreguntaForm
     model = Question
     login_url = reverse_lazy('usuarios_app:user-login')

     def get_success_url(self):
        return reverse_lazy('questions_app:questions_all')

     def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
     
     def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Question, pk=pk)
     
     def get_context_data(self, **kwargs):
         return super().get_context_data(**kwargs)

     def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


     def form_valid(self, form):
        titulo = form.cleaned_data['titulo']
        responses = form.cleaned_data['responses_field']
        quest=self.get_object()
        if quest.title != titulo:
            quest.title = titulo
        quest.save()
        PosibleAnswers.objects.filter(question=quest).delete()
        for response in responses:
            PosibleAnswers.objects.get_or_create(
                texto=response,
                question=quest
            )
        
        return super(QuestionUpdateView, self).form_valid(form)
     


def delete_question(request, pk):
    question = Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect(reverse_lazy('questions_app:questions_all'))


class ListQuestionsBlock(LoginRequiredMixin, ListView):
    template_name = 'questions/list_blocks.html'
    paginate_by = 10
    model = QuestionBlock
    context_object_name = 'lista_blocks'
    login_url = reverse_lazy('usuarios_app:user-login')


    def get_queryset(self, *args, **kwargs):
        lista_blocks = super(ListQuestionsBlock, self).get_queryset(*args, **kwargs)
        lista_blocks = lista_blocks.order_by("importance")
        return lista_blocks
    
    def get_context_data(self, **kwargs):
        context =  super(ListQuestionsBlock, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.all
        return context


class BlockCreateView(LoginRequiredMixin, CreateView):
    template_name = 'questions/add_block.html'
    model = QuestionBlock
    form_class = BlockForm
    success_url  = reverse_lazy('questions_app:blocks_all')
    login_url = reverse_lazy('usuarios_app:user-login')

    def form_valid(self, form):
        quest = form.cleaned_data['question']
        for title in quest:
            question = Question.objects.get(title=title)
            question.blocks.clear()
            question.save()    
        return super(BlockCreateView, self).form_valid(form)

class BlockUpdateView(LoginRequiredMixin, UpdateView):
    model = QuestionBlock
    template_name = "questions/update_block.html"
    form_class = BlockForm
    success_url  = reverse_lazy('questions_app:blocks_all')
    login_url = reverse_lazy('usuarios_app:user-login')

    def form_valid(self, form):
        quest = form.cleaned_data['question']
        for title in quest:
            question = Question.objects.get(title=title)
            question.blocks.clear()
            question.save()    
        return super(BlockUpdateView, self).form_valid(form)
    
def delete_block(request, pk):
    block = QuestionBlock.objects.get(id=pk)
    block.delete()
    return HttpResponseRedirect(reverse_lazy('questions_app:blocks_all'))
