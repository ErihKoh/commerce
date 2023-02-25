from django import forms
from .models import Auction

CATEGORIES = (
        ('no-category', 'no-category'),
        ('digital', 'digital'),
        ('fashion', 'fashion'),
        ('home', 'home'),
    )


class AuctionForm(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ['name', 'description', 'image_url', 'price', 'end_date', 'category']
        widgets = {
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'category': forms.Select(choices=CATEGORIES,  attrs={'class': 'form-control'}),
            'image_url': forms.ClearableFileInput(attrs={'multiple': True}),
        }
        initial = {'category': 'no-category'}
