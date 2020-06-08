from django import forms


class CartAddForm(forms.Form):
    """Form for adding products to a cart."""

    quantity = forms.IntegerField(label='',
                                  widget=forms.NumberInput(
                                      attrs={
                                          'class': 'cart-form__input',
                                          'value':'1'
                                      }
                                  ))
    update = forms.BooleanField(required=False,
                                initial=False, widget=forms.HiddenInput)


class CartAddButton(forms.Form):
    """Form for adding products from a list page."""

    quantity = 1
    update = forms.BooleanField(required=False,
                                initial=False, widget=forms.HiddenInput)
