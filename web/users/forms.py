from django import forms
from django.contrib.auth.models import User
from users.models import Profile


class SigninForm(forms.Form):
    """Signin form."""

    username = forms.CharField(max_length=50, label='',
                               widget=forms.TextInput(
                                   attrs={
                                       'placeholder': 'Username',
                                       'class': 'auth-form__input'
                                   }
                               ))
    password = forms.CharField(max_length=50, label='',
                               widget=forms.PasswordInput(
                                   attrs={
                                       'placeholder': 'Password',
                                       'class': 'auth-form__input'
                                   }
                               ))


class SignupForm(forms.Form):
    """Signup form."""

    username = forms.CharField(max_length=50, label='',
                               widget=forms.TextInput(
                                   attrs={
                                       'placeholder': 'Username',
                                       'class': 'auth-form__input'
                                   }
                               ))
    password = forms.CharField(max_length=50, label='',
                               widget=forms.PasswordInput(
                                   attrs={
                                       'placeholder': 'Password',
                                       'class': 'auth-form__input'
                                   }
                               ))
    password_r = forms.CharField(max_length=50, label='',
                                 widget=forms.PasswordInput(
                                     attrs={
                                         'placeholder': 'Repeat password',
                                         'class': 'auth-form__input'
                                     }
                                 ))


class UserForm(forms.ModelForm):
    """User update form."""
    first_name = forms.CharField(max_length=50, label='',
                                 widget=forms.TextInput(
                                     attrs={
                                         'placeholder': 'First name',
                                         'class': 'update-form__input'
                                     }
                                 ), required=False)
    last_name = forms.CharField(max_length=50, label='',
                                widget=forms.TextInput(
                                    attrs={
                                        'placeholder': 'Last name',
                                        'class': 'update-form__input'
                                    }
                                ), required=False)
    email = forms.CharField(max_length=50, label='',
                            widget=forms.EmailInput(
                                attrs={
                                    'placeholder': 'Email',
                                    'class': 'update-form__input'
                                }
                            ), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    """Profile update form."""
    birth_date = forms.DateField(label='',
                                 widget=forms.DateInput(
                                     attrs={
                                         'class': 'update-form__input',
                                         'type': 'date',
                                         'placeholder': 'Birth date yyyy-dd-mm'
                                     }
                                 ), required=False)
    address = forms.CharField(max_length=50, label='',
                              widget=forms.TextInput(
                                  attrs={
                                      'placeholder': 'Address',
                                      'class': 'update-form__input'
                                  }
                              ), required=False)
    biography = forms.CharField(max_length=50, label='',
                                widget=forms.Textarea(
                                    attrs={
                                        'placeholder': 'Biography',
                                        'class': 'update-form__text-area'
                                    }
                                ), required=False)

    class Meta:
        model = Profile
        fields = ['birth_date', 'address', 'biography']


class PasswordForm(forms.Form):
    """User password update form."""

    password = forms.CharField(max_length=50, label='',
                               widget=forms.PasswordInput(
                                   attrs={
                                       'placeholder': 'Password',
                                       'class': 'update-form__input'
                                   })
                               )
    password_r = forms.CharField(max_length=50, label='',
                                 widget=forms.PasswordInput(
                                     attrs={
                                         'placeholder': 'Repeat password',
                                         'class': 'update-form__input'
                                     })
                                 )
