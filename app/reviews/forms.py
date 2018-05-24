from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Review


class PostForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = (
            'item',
            'title',
            'content',
        )
        widgets = {
            'content': SummernoteWidget()
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = self.fields['item'].queryset.filter(user=user, is_purchase=True)
