from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, FormMixin, DeletionMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    DeleteView,
    UpdateView,
)

from .models import Question, PosibleAnswers, QuestionBlock
from .forms import PreguntaForm, PosibleAnswersFormSet, BlockForm, BlockUpdateForm
from applications.usuarios.models import User
from applications.contexts.models import Context
from applications.answers.models import Answer


class ListQuestions(LoginRequiredMixin, DeletionMixin, ListView):
    template_name = 'questions/list_questions.html'
    paginate_by = 20
    model = Question
    context_object_name = 'lista_questions'
    login_url = reverse_lazy('usuarios_app:user-login')

    def get_queryset(self, *args, **kwargs):
        lista_questions = super(ListQuestions, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('search')
        if query:
            lista_questions = lista_questions.filter(title__icontains=query).order_by("-create") 
        else:
            lista_questions = lista_questions.order_by("-create")
        return lista_questions
    

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
        user = User.objects.get(id=self.request.user.id)
        quest=Question.objects.create(
            title=titulo,
            creator=user
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

def clone_question(request, pk):
    question = Question.objects.get(id=pk)
    quest = Question.objects.create(
        title = question.title,
    )
    quest.save()
    answers = PosibleAnswers.objects.filter(question=question)
    for answer in answers:
        PosibleAnswers.objects.create(
            texto = answer.texto,
            question = quest
        )
    return HttpResponseRedirect(reverse_lazy('questions_app:questions_all'))


class ListQuestionsBlock(LoginRequiredMixin, ListView):
    template_name = 'questions/list_blocks.html'
    paginate_by = 10
    model = QuestionBlock
    context_object_name = 'lista_blocks'
    login_url = reverse_lazy('usuarios_app:user-login')


    def get_queryset(self, *args, **kwargs):
        lista_blocks = super(ListQuestionsBlock, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('search')
        if query:
            lista_blocks = lista_blocks.filter(block__icontains=query).order_by("-create") 
        else:
            lista_blocks = lista_blocks.order_by("-create")
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

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(QuestionBlock, pk=pk)
     
    def form_valid(self, form):
        quest = form.cleaned_data['question']
        if form.cleaned_data['frecuency'] == 'O':
            form.instance.active = True
 

        return super(BlockCreateView, self).form_valid(form)

class BlockUpdateView(LoginRequiredMixin, UpdateView, DeletionMixin):
    model = QuestionBlock
    template_name = "questions/update_block.html"
    form_class = BlockForm
    success_url  = reverse_lazy('questions_app:blocks_all')
    login_url = reverse_lazy('usuarios_app:user-login')
        
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
     
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(QuestionBlock, pk=pk)
     
    def get_context_data(self, **kwargs):
         return super().get_context_data(**kwargs)
    
    def compare(self, time, days, duration, frecuency, active):
        self.object = self.get_object()
        if self.object.time != time or self.object.days != days or self.object.duration != duration or self.object.frecuency != frecuency or self.object.active != active:
            return True
        else:
            return False


    def form_valid(self, form):
        self.object = self.get_object()
        time = form.cleaned_data['time']    
        days = form.cleaned_data['days']
        duration = form.cleaned_data['duration']
        frecuency = form.cleaned_data['frecuency']
        active = form.cleaned_data['active']
        if self.compare(time, days, duration, frecuency, active):
            self.udpate_block(form)
            return self.delete(self.request)
        else:
            return super(BlockUpdateView, self).form_valid(form)
        
    
    def udpate_block(self, form):
        block = form.cleaned_data['block']
        importance = form.cleaned_data['importance']
        questions = form.cleaned_data['question']
        contexts = form.cleaned_data['context']
        time = form.cleaned_data['time']    
        days = form.cleaned_data['days']
        duration = form.cleaned_data['duration']
        frecuency = form.cleaned_data['frecuency']
        active = form.cleaned_data['active']
        blo = QuestionBlock.objects.create(
            block = block,
            frecuency = frecuency,
            importance = importance,
            time = time,
            days = days,
            duration = duration,
            active = active,
        )
        blo.save()
        for question in questions:
            question.blocks.add(blo)
        for context in contexts:
            context.block.add(blo)
        answers = Answer.objects.filter(block=self.get_object())
        for answer in answers:
            answer.block = blo
            answer.save()

def delete_block(request, pk):
    block = QuestionBlock.objects.get(id=pk)
    block.delete()
    return HttpResponseRedirect(reverse_lazy('questions_app:blocks_all'))


def clone_block(request, pk):
    block = QuestionBlock.objects.get(id=pk)
    blo = QuestionBlock.objects.create(
        block = block.block,
        frecuency = block.frecuency,
        importance = block.importance,
        time = block.time,
        days = block.days,
        duration = block.duration
    )
    blo.save()
    questions = Question.objects.filter(blocks=block)
    for question in questions:
        question.blocks.add(blo)
    contexts = Context.objects.filter(block=block)
    for context in contexts:
        context.block.add(blo)
    return HttpResponseRedirect(reverse_lazy('questions_app:blocks_all'))



        

