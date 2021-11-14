from django import forms


class FavoriteForm(forms.Form):
    product_id = forms.CharField()
