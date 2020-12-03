import os

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, reverse, render
from django.views.generic import CreateView, View

from jobs.forms.account import UserLoginForm, UserRegisterForm, ProfileForm, CustomPasswordChangeForm
from jobs.views.override import LoginRequiredMixinOverride


class MyRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = os.path.join('jobs', 'account', 'register.html')
    success_url = 'login'
    success_message = 'Вы успешно зарегистировались!'


class MyLoginView(LoginView):
    form_class = UserLoginForm
    redirect_authenticated_user = True
    template_name = os.path.join('jobs', 'account', 'login.html')


class MyProfileView(LoginRequiredMixinOverride, View):
    def get(self, request):
        user_form = ProfileForm(instance=request.user)
        return render(request, os.path.join('jobs', 'account', 'profile.html'), {'form': user_form})

    def post(self, request):
        user_form = ProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.info(request, 'Профиль был обновлен')
        else:
            messages.error(request, 'Проверьте правильность введенной информации!')
            return render(request, os.path.join('jobs', 'account', 'profile.html'), {'form': user_form})
        return redirect(reverse('myprofile'))


class MyPasswordChangeView(LoginRequiredMixinOverride, View):
    def get(self, request):
        change_password_form = CustomPasswordChangeForm(request.user)
        return render(request, os.path.join('jobs', 'account', 'change_password.html'), {'form': change_password_form})

    def post(self, request):
        change_password_form = CustomPasswordChangeForm(request.user, request.POST)
        if change_password_form.is_valid():
            change_password_form.save()
            update_session_auth_hash(request, change_password_form.user)
            messages.info(request, 'Пароль был изменен')
        else:
            messages.error(request, 'Проверьте правильность введенной информации!')
            return render(request, os.path.join('jobs', 'account', 'change_password.html'),
                          {'form': change_password_form})
        return redirect(reverse('myprofile'))
