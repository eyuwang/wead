from django import forms

class NoValidateField(forms.ChoiceField):
    def validate(self, value):
        pass            

class ArticleForm(forms.Form):
    category = NoValidateField(label='category', choices=[])
    author = forms.CharField(max_length=30)
    title = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)

class ArticlesForm(forms.Form):
    category = NoValidateField(label='category', choices=[])
    body = forms.CharField(widget=forms.Textarea)

