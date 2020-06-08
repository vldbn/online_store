from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddForm(forms.Form):
    """Form for adding products to a cart."""

    quantity = forms.IntegerField(label='',
                                  widget=forms.NumberInput(
                                      attrs={
                                          'class':'cart-form__input'
                                      }
                                  ))
    update = forms.BooleanField(required=False,
                                initial=False, widget=forms.HiddenInput)

class CartAddButton(forms.Form):
    quantity = 1
    update = forms.BooleanField(required=False,
                                initial=False, widget=forms.HiddenInput)
