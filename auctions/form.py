from django import forms
from .models import Auction

CATEGORIES = (
        ('no-category', 'no-category'),
        ('digital', 'digital'),
        ('fashion', 'fashion'),
        ('home', 'home'),
    )


class AuctionForm(forms.ModelForm):
    price = forms.DecimalField(initial=0.00)
    class Meta:
        model = Auction
        fields = ['name', 'description', 'image_url', 'price', 'end_date', 'category']
        widgets = {
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'category': forms.Select(choices=CATEGORIES,  attrs={'class': 'form-control'}),
            'image_url': forms.ClearableFileInput(attrs={'multiple': True}),
        }
        initial = {'category': 'no-category', }



class EditAuctionForm(forms.ModelForm):
    is_available = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    class Meta:
        model = Auction
        fields = ['name', 'description', 'price', 'is_available']
        widgets = {
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }        
