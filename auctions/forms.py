from django import forms


category_choice ={
    (1, "no category"),
    (2, "digital"),
    (3, "fashion"),
    (4, "home"),
    (5, "car"),
}

class NewAuction(forms.Form):
    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Product name'}))
    description = forms. CharField(widget=forms.TextInput(attrs={'placeholder': 'Product description'}))
    bid = forms. CharField(widget=forms.TextInput(attrs={'placeholder': 'Start price'}))
    category = forms.ChoiceField(choices = category_choice, initial=1, widget=forms.Select(), required=True)
    img_url = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'image url'}))

    