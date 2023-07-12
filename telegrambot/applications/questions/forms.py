from django import forms
from django.forms import formset_factory
from django.core.exceptions import ValidationError
from .models import Question, PosibleAnswers, QuestionBlock
from applications.contexts.models import Context



class PreguntaForm(forms.Form):
    titulo = forms.CharField(widget=forms.TextInput(attrs={'name':'titulo', 'placeholder': 'How are you?', 'size':'140'}))
    responses = forms.CharField(widget=forms.Textarea(attrs={'name':'responses', 'placeholder':'Please write one response per line', 'rows':10, 'cols':60 }))

    def clean(self):
        cd = self.cleaned_data 
        clean_responses = cd.get("responses").replace('\r', '')
        response_list = list()
        for response in clean_responses.split('\n'):
            if response:
                clean_response = response.strip()
                if clean_response:
                    response_list.append(response)
        responses_field = list(dict.fromkeys(response_list))
        if len(responses_field) < 2:
            raise ValidationError("You must specify at least two different responses")
        self.cleaned_data['responses_field'] = [PosibleAnswers(texto=r) for r in responses_field]


PosibleAnswersFormSet = formset_factory(PreguntaForm, extra=1)

class BlockForm(forms.ModelForm):

    class Meta:
        model = QuestionBlock
        fields = (
            'block',
            'question',
            'context',
            'active',
            'frecuency',
            'importance',
        )
    question = forms.ModelMultipleChoiceField(queryset=Question.objects.all().order_by('-create'), widget=forms.CheckboxSelectMultiple)
   
