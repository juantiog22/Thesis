from django import forms
from django.contrib.auth import authenticate
from .models import User

class UserRegisterForm(forms.ModelForm):

    username = forms.CharField(
        label = 'username',
        required = True,
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
            }
        ))
    
    email = forms.EmailField(
        label = 'email',
        required = True,
        widget=forms.TextInput(
            attrs={
                "placeholder" : "User@gmail.com",                
            }
        ))

    password1 = forms.CharField(
        label = 'Password',
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )

    password2 = forms.CharField(
        label = 'Password',
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat password'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', )


    def clean(self):

        usernames = User.objects.all()
        userna = User.objects.filter(username=self.cleaned_data['username']).first()
        userem = User.objects.filter(email=self.cleaned_data['email']).first()

        if userna is not None:
            if usernames.contains(userna):
                raise forms.ValidationError('The user already exists in the system. Please choose another username')
        
        if userem is not None:
            if usernames.contains(userem):
                raise forms.ValidationError('The user already exists in the system. Please choose another email')

        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match')

        if len(self.cleaned_data['password1']) < 8:
            raise forms.ValidationError('Password must contains at least 8 characters')
        
        

class LoginForm(forms.Form):
    username = forms.CharField(
        label = 'username',
        required = True,
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",
                "style" : "{margin: 10px}",                
            }
        ))
    
    password = forms.CharField(
        label = 'Password',
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('User data is not correct')

        return self.cleaned_data
    


class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label = 'Password',
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Actual password'
            }
        )
    )
    password2 = forms.CharField(
        label = 'Password',
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'New password'
            }
        )
    )
    
    def clean(self):

        cleaned_data = super(UpdatePasswordForm, self).clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        
    
        if len(self.cleaned_data['password2']) < 8:
            raise forms.ValidationError('Password must contains at least 8 characters')
        
        return self.cleaned_data
