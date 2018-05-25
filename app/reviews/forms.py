from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Review


class AddReviewForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # user가 구매완료한 제품만 표시
        self.fields['item'].queryset = self.fields['item'].queryset.filter(user=request.user, is_purchase=True)

        self.fields['item'].label = '제품명'

        class_update_fields = ('item', 'title')
        for field in class_update_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Review
        fields = (
            'item',
            'title',
            'content',
        )
        widgets = {
            'content': SummernoteWidget(),
        }
