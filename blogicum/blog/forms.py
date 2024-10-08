from django import forms

from .models import User, Comments, Post


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',)


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        empty_value_display = 'Не задано'
        fields = ('title',
                  'text',
                  'image',
                  'pub_date',
                  'location',
                  'category')
        widgets = {'pub_date': forms.DateTimeInput(
            attrs={'type': 'datetime-local'})}
