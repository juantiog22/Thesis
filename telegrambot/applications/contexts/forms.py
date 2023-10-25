from django import forms
from django.forms import formset_factory
from django.core.exceptions import ValidationError
from .models import Context, Message



class ContextForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'name':'name', 'placeholder': 'Write the context name', 'size':'140'}))
    messages = forms.CharField(widget=forms.Textarea(attrs={'name':'messaged', 'id': 'messages', 'placeholder':'Please write one message per line', 'rows':10, 'cols':60 }))

    def clean(self):
        cd = self.cleaned_data 
        clean_messages = cd.get("messages").replace('\r', '')
        message_list = list()
        for message in clean_messages.split('\n'):
            if message:
                clean_response = message.strip()
                if clean_response:
                    message_list.append(message)
        messages_field = list(dict.fromkeys(message_list))
        self.cleaned_data['messages_field'] = [Message(text=r) for r in messages_field]

