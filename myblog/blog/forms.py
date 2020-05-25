from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Comment, Post


class WidgetMixinForm(forms.ModelForm):
    """Mixin для переопределения отображения
       форм на 'form-control' bootstrap
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreatePostForm(WidgetMixinForm, forms.ModelForm):
    """class формы создания posts"""
    class Meta:
        model = Post
        fields = ('title', 'body',)


class AuthUserForm(WidgetMixinForm, AuthenticationForm, forms.ModelForm):
    """class формы авторизации users"""

    class Meta:
        model = User
        fields = ('username', 'password',)


class RegisterUserForm(WidgetMixinForm, UserCreationForm):
    """class формы регистрации users
       UserCreationForm наследник Modelform
    """
    email = forms.EmailField(max_length=100, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    """class формы создания comments"""
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            "body": forms.Textarea(attrs={"class": "form-control",
                                          'rows': 5, })
        }


class EmailPostForm(forms.Form):
    """class формы поделиться posts по email"""
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea)
