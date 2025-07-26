from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label="Menge"
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
    rental_start = forms.DateField(
        required=True,
        widget=forms.HiddenInput
    )
    rental_end = forms.DateField(
        required=True,
        widget=forms.HiddenInput
    )

