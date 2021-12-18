from django.forms import ModelForm
from .models import Group, Post
from django.forms.widgets import Textarea, Select


'''class PostForm(ModelForm):
    text = forms.CharField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)'''


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['text', 'group']

    widgets = {
            "text": Textarea(attrs={
                'name': 'text', 'cols': '40', 'rows': '10',
                'class': 'form-control', 'required id': 'id_text'
            }),
            "group": Select(attrs={
                'name': 'group', 'class': 'form-control', 'id': 'id_group'
            }),
        }