import os

from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import View

from jobs.models import Resume, Application
from jobs.forms.resume import ResumeForm
from jobs.views.override import LoginRequiredMixinOverride


class MyResumeView(LoginRequiredMixinOverride, View):
    def get(self, request):
        user_resume = Resume.objects.filter(user=request.user).first()
        context = {}
        if user_resume:
            context['form'] = ResumeForm(instance=user_resume)
        return render(request, os.path.join('jobs', 'resume', 'resume.html'), context)

    def post(self, request):
        user_resume = Resume.objects.filter(user=request.user).first()
        user_resume_form = ResumeForm(request.POST, instance=user_resume)
        if user_resume_form.is_valid():
            user_resume_form.save()
            messages.info(request, 'Резюме было обновлено')
        else:
            messages.error(request, 'Проверьте правильность введенной информации!')
            context = {'form': user_resume_form}
            return render(request, os.path.join('jobs', 'resume', 'resume.html'), context)
        return redirect(reverse('myresume'))


class MyResumeCreateView(LoginRequiredMixinOverride, View):
    def get(self, request):
        user_resume = Resume.objects.filter(user=request.user).first()
        if user_resume:
            return redirect(reverse('myresume'))
        context = {
            'form': ResumeForm(
                initial={
                    'name': request.user.first_name,
                    'surname': request.user.last_name,
                }),
            'is_new_resume': True,
        }
        return render(request, os.path.join('jobs', 'resume', 'resume.html'), context)

    def post(self, request):
        user_resume_form = ResumeForm(request.POST)
        if user_resume_form.is_valid():
            user_resume_instance = user_resume_form.save(commit=False)
            user_resume_instance.user = request.user
            user_resume_instance.save()
            messages.info(request, 'Резюме было создано')
        else:
            messages.error(request, 'Проверьте правильность введенной информации!')
            context = {'form': user_resume_form, 'is_new_resume': True}
            return render(request, os.path.join('jobs', 'resume', 'resume.html'), context)
        return redirect(reverse('myresume'))


class MyResumeDeleteView(LoginRequiredMixinOverride, View):
    def post(self, request):
        Resume.objects.filter(user=request.user).delete()
        messages.warning(request, 'Резюме было удалено')
        return redirect(reverse('myresume'))


class MyResumePublicView(LoginRequiredMixinOverride, View):
    def get(self, request, pk):
        next_url = request.GET.get('next')
        if next_url is None:
            next_url = reverse('main')
        user_resume = Resume.objects.filter(user__id=pk).first()
        if user_resume is None:
            messages.warning(request, 'Резюме не было найдено')
            return redirect(next_url)
        query_user_application = Application.objects.filter(
            vacancy__company__owner=request.user,
            user__id=pk)
        if not (pk == request.user.id or query_user_application.first() is not None):
            messages.error(request, 'У вас нет права на просмотр резюме')
            return redirect(next_url)
        context = {'resume': user_resume}
        return render(request, os.path.join('jobs', 'resume', 'resume_public.html'), context)
