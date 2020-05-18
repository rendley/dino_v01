from django import forms
from django.contrib.auth.models import User

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
    class Meta:
        model = Post
        fields = ('title', 'body',)


class AuthUserForm(WidgetMixinForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)


class RegisterUserForm(WidgetMixinForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',  'email', 'password',)


class CommentForm(WidgetMixinForm, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class EmailPostForm(WidgetMixinForm, forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea)



