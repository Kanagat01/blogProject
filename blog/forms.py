from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=25)
    email = forms.EmailField(label='Ваш Email')
    to = forms.EmailField(label='Email получателя')
    comments = forms.CharField(label='Комментарии', required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()
