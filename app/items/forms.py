from django import forms

from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'name',
            'purchase_url',
            'price',
            'category',
            'img_url',
            'public_visibility',
        )

    def save(self, commit=True, *args, **kwargs):
        if not self.instance.pk and commit:
            user = kwargs.pop('user', None)
            if not user:
                raise ValueError('User field is required')
            self.instance.user = user

        return super().save(*args, **kwargs)
