from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Review, ReviewComment


class ReviewForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # user가 구매완료한 제품만 표시
        self.fields['item'].queryset = self.fields['item'].queryset.filter(user=request.user, is_purchase=True)
        self.fields['item'].label = '제품명'
        self.fields['item'].label_from_instance = self.label_from_instance

        class_update_fields = ('item', 'title')
        for field in class_update_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    @staticmethod
    def label_from_instance(self):
        return f'{self.name}'

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


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = (
            'content',
        )
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'cols': 115,
                    'rows': 3,
                    'class': 'form-control',
                    'placeholder': "댓글을 입력해주세요",
                }
            )
        }
