from django import forms
from store.models import Rating


class RatingForm(forms.Form):
    """Rating form"""

    rate = forms.IntegerField(label='', min_value= 0, max_value=5,
                              widget=forms.NumberInput(
                                  attrs={
                                      'class': 'rating-form__input',
                                      'placeholder':'0'
                                  }
                              ))
