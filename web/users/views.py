from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from users import forms


class ProfileView(LoginRequiredMixin, View):
    """Profile view"""

    def get(self, request):
        # TODO add all categories
        user = User.objects.get(username=request.user)
        context = {
            'user': user
        }
        return render(request, 'users/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, View):
    """Profile update view."""

    def get(self, request):
        # TODO add all categories
        user = User.objects.get(username=request.user.username)
        user_form = forms.UserForm(instance=user)
        profile_form = forms.ProfileForm(instance=user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'users/profile_update.html', context)

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        user_form = forms.UserForm(request.POST, instance=user)
        profile_form = forms.ProfileForm(request.POST, instance=user.profile)

        if user_form.is_valid() or profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:profile')
        else:
            return redirect('users:update-profile')


class PasswordUpdateView(LoginRequiredMixin, View):
    """Password update view."""

    def get(self, request):
        form = forms.PasswordForm()
        context = {
            'form': form
        }
        return render(request, 'users/profile_update_pass.html', context)

    def post(self, request):
        form = forms.PasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            password = form.cleaned_data.get('password')
            password_r = form.cleaned_data.get('password_r')
            if password == password_r:
                user.set_password(password)
                user.save()
                return redirect('users:signin')
            else:
                messages.add_message(request, messages.INFO,
                                     'Passwords do not match.')
                return redirect('users:update-password')


class SigninView(View):
    """Sign in view. """

    def get(self, request):
        if request.user.is_authenticated:
            #TODO change redirect destination, when add Products.
            return redirect('home')

        form = forms.SigninForm()
        context = {
            'form': form
        }
        return render(request, 'users/signin.html', context)

    def post(self, request):
        form = forms.SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is None:
                messages.add_message(request, messages.INFO,
                                     'User does not exist.')
                return redirect('users:signin')
            else:
                login(request, user)
                # TODO change redirect destination, when add Products.
                return redirect('home')


class SignupView(View):
    """Sign up view."""

    def get(self, request):
        if request.user.is_authenticated:
            # TODO change redirect destination, when add Products.
            return redirect('home')

        form = forms.SignupForm()
        context = {
            'form': form
        }
        return render(request, 'users/signup.html', context)

    def post(self, request):
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            password_r = form.cleaned_data.get('password_r')

            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                user = None

            if user is not None:
                messages.add_message(request, messages.INFO,
                                     'User is already exist.')
                return redirect('users:signup')
            else:
                if password == password_r:
                    User.objects.create_user(
                        username=username,
                        password=password
                    )
                    return redirect('users:signin')
                else:
                    messages.add_message(request, messages.INFO,
                                         'Passwords do not match.')
                    return redirect('users:signup')


@login_required
def logout_view(request):
    """Logout view. """

    logout(request)
    return redirect('users:signin')
