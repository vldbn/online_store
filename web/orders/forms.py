from django import forms
from users.models import Profile


class OrderProfileForm(forms.ModelForm):
    """Order form."""

    address = forms.CharField(max_length=100, label='',
                              widget=forms.TextInput(
                                  attrs={
                                      'placeholder': 'Address',
                                      'class': 'update-form__input'
                                  }
                              ))
    postal_code = forms.CharField(max_length=20, label='',
                                  widget=forms.TextInput(
                                      attrs={
                                          'placeholder': 'Postal code',
                                          'class': 'update-form__input'
                                      }
                                  ))
    city = forms.CharField(max_length=100, label='',
                           widget=forms.TextInput(
                               attrs={
                                   'placeholder': 'City',
                                   'class': 'update-form__input'
                               }
                           ))

    class Meta:
        model = Profile
        fields = ['address', 'postal_code', 'city']