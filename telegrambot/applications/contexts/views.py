from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, FormMixin, DeletionMixin
from django.core.paginator import Paginator
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    DeleteView,
    UpdateView,
)

from .models import Context, Message
from .forms import ContextForm

class ListContexts(LoginRequiredMixin, DeletionMixin, ListView):
    template_name = 'contexts/list_contexts.html'
    paginate_by = 10
    model = Context
    context_object_name = 'lista_contexts'
    login_url = reverse_lazy('usuarios_app:user-login')



    def get_queryset(self, *args, **kwargs):
        lista_contexts = super(ListContexts, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('search')
        if query:
            lista_contexts = lista_contexts.filter(name__icontains=query).order_by("-id")
        else:
            lista_contexts = lista_contexts.order_by("-id")
        return lista_contexts

   
class NewContextView(LoginRequiredMixin, FormView):
    template_name = 'contexts/add_context.html'
    form_class = ContextForm
    login_url = reverse_lazy('usuarios_app:user-login')

    def get_success_url(self):
        return reverse_lazy('contexts_app:contexts_all')

    def get_queryset(self):
        context_name = self.kwargs['text']
        lista = Message.objects.filter(
            context__name=context_name
        )
        return lista
    
    def form_valid(self, form):
        name = form.cleaned_data['name']
        messages = form.cleaned_data['messages_field']
        context=Context.objects.create(
            name=name 
        )
        for message in messages:
            Message.objects.create(
                text=message,
                context=context
            )
            
        return super(NewContextView, self).form_valid(form)


class ContextUpdateView(LoginRequiredMixin, FormMixin, DetailView):
     template_name = 'contexts/update_context.html'
     form_class = ContextForm
     model = Context
     login_url = reverse_lazy('usuarios_app:user-login')

     def get_success_url(self):
        return reverse_lazy('contexts_app:contexts_all')

     def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
     
     def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Context, pk=pk)
     
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
        name = form.cleaned_data['name']
        messages = form.cleaned_data['messages_field']
        context=self.get_object()
        if context.name != name:
            context.name = name
        context.save()
        Message.objects.filter(context=context).delete()
        for message in messages:
            Message.objects.get_or_create(
                text=message,
                context=context
            )
        
        return super(ContextUpdateView, self).form_valid(form)
     
    
def delete(request, pk):
    context = Context.objects.get(id=pk)
    context.delete()
    return HttpResponseRedirect(reverse_lazy('contexts_app:contexts_all'))

def clone_context(request, pk):
    context = Context.objects.get(id=pk)
    con = Context.objects.create(
        name = context.name,
    )
    con.save()
    messages = Message.objects.filter(context=context)
    for message in messages:
        Message.objects.create(
            text = message.text,
            context = con
        )
    return HttpResponseRedirect(reverse_lazy('contexts_app:contexts_all'))