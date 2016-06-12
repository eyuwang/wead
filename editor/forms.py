# -*- coding: utf-8 -*
from django import forms
from editor.models import Articles, Users, UploadFile
from registration.forms import RegistrationForm


class UserRegistrationForm(RegistrationForm):
    email = forms.EmailField(
        required = True
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'username',
            }
        ),
        required = True
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'first_name',
            }
        ),
        required = True
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'last_name',
            }
        ),
        required = True
    )

    user_type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'user_typee',
            }
        ),
        required = True
    )

    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'user_type']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'text_editor_title',
                'placeholder': '给个标题吧....'
            }
        ),
        required = True
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'text_editor_pane',
                'placeholder': '加点内容吧....',
                'rows': 100
            }
        ),
        initial='加点内容吧....',
        required = True
    )

    class Meta:
        model = Articles 
        #fields = ['author', 'title', 'content']
        fields = ['title', 'content']

class UploadFileForm(forms.ModelForm):
    file_uploaded = forms.FileField()
    user = forms.CharField()

    class Meta:
        model = UploadFile 
        fields = ['file_uploaded', 'user']
