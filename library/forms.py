from django import forms

from .models import Library

class NoValidateChoiceField(forms.ChoiceField):
    def validate(self, value):
        pass            

class NoValidateModelChoiceField(forms.ModelChoiceField):
    def validate(self, value):
        pass            

class LibraryForm(forms.ModelForm):
    CHOICES = (
        ('photo', 'photo'),
        ('audio', 'audio')
    )
    type = forms.ChoiceField(choices=CHOICES)
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=200)
    code = forms.IntegerField()
    parent = NoValidateModelChoiceField(queryset=Library.objects.all())
    
class PhotoForm(forms.Form):
    library = NoValidateChoiceField(label='library', choices=[])
    author = forms.CharField(max_length=30)
    title = forms.CharField(max_length=100)
    file = forms.FileField()

class PhotosForm(forms.Form):
    library = NoValidateChoiceField(label='library', choices=[])
    files = forms.FileField()
    
class AudioForm(forms.Form):
    library = NoValidateChoiceField(label='library', choices=[])
    author = forms.CharField(max_length=30)
    title = forms.CharField(max_length=100)
    file = forms.FileField()

class AudiosForm(forms.Form):
    library = NoValidateChoiceField(label='library', choices=[])
    files = forms.FileField()
