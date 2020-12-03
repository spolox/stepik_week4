import os

from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import View

from jobs.models import Vacancy, Company, Application
from jobs.forms.company import CompanyForm
from jobs.forms.vacancy import VacancyForm
from jobs.views.override import LoginRequiredMixinOverride, HasCompanyRequiredMixin


class MyCompanyView(LoginRequiredMixinOverride, View):
    def get(self, request):
        user = request.user
        user_company = Company.objects.filter(owner=user).first()
        user_company_form = None
        context = {}
        if user_company is not None:
            user_company_form = CompanyForm(instance=user_company)
        context['form'] = user_company_form
        return render(request, os.path.join('jobs', 'my_company', 'company.html'), context)

    def post(self, request):
        user = request.user
        user_company = Company.objects.filter(owner=user).first()
        user_company_form = CompanyForm(request.POST, request.FILES, instance=user_company)
        if user_company_form.is_valid():
            user_company_form.save()
            messages.info(request, 'Информация о компании обновлена')
        else:
            messages.error(request, 'Проверьте правильность введенной информации!')
            return render(request, os.path.join('jobs', 'my_company', 'company.html'), {'form': user_company_form})
        return redirect(reverse('mycompany'))


class MyCompanyCreateView(LoginRequiredMixinOverride, View):
    def get(self, request):
        user = request.user
        user_company = Company.objects.filter(owner=user).first()
        if user_company is not None:
            return redirect(reverse('mycompany'))
        user_company_form = CompanyForm()
        context = {'form': user_company_form, 'is_new_company': True}
        return render(request, os.path.join('jobs', 'my_company', 'company.html'), context)

    def post(self, request):
        user_company_form = CompanyForm(request.POST, request.FILES)
        if user_company_form.is_valid():
            user_company_instance = user_company_form.save(commit=False)
            user_company_instance.owner = request.user
            user_company_instance.save()
            messages.info(request, 'Компания была создана')
        else:
            messages.error(request, 'Проверьте правильность введенной информации!')
            context = {'form': user_company_form, 'is_new_company': True}
            return render(request, os.path.join('jobs', 'my_company', 'company.html'), context)
        return redirect(reverse('mycompany'))


class MyCompanyDeleteView(LoginRequiredMixinOverride, View):
    def post(self, request):
        Company.objects.filter(owner=request.user).delete()
        messages.warning(request, 'Компания была удалена')
        return redirect(reverse('mycompany'))


class MyCompanyVacancyListView(LoginRequiredMixinOverride, HasCompanyRequiredMixin, View):
    def get(self, request):
        vacancy_list = Vacancy.objects.filter(company__owner=self.request.user).all().prefetch_related('applications')
        if vacancy_list.count() == 0:
            messages.info(self.request, 'У вас пока нет вакансий, но вы можете создать первую!')
        return render(request, os.path.join('jobs', 'my_company', 'company_vacancy_list.html'),
                      {'vacancy_list': vacancy_list})


class MyCompanyVacancyView(LoginRequiredMixinOverride, HasCompanyRequiredMixin, View):
    def get(self, request, pk):
        vacancy_choice = Vacancy.objects.filter(id=pk).first()
        context = {
            'pk': pk,
            'vacancy': vacancy_choice,
        }
        if vacancy_choice:
            if vacancy_choice.company.owner != self.request.user:
                messages.error(self.request, 'У вас нет права на редактирование выбранной вакансии!')
                return redirect(reverse('mycompany-vacancy-list'))
            context['form'] = VacancyForm(instance=vacancy_choice)
        else:
            messages.error(self.request, 'Такой вакансии не существует в базе данных!')
            return redirect(reverse('mycompany-vacancy-list'))
        return render(request, os.path.join('jobs', 'my_company', 'company_vacancy_edit.html'), context)

    def post(self, request, pk):
        user_vacancy = Vacancy.objects.filter(id=pk).first()
        user_vacancy_form = VacancyForm(request.POST, instance=user_vacancy)
        if user_vacancy_form.is_valid():
            user_vacancy_form.save()
            messages.info(request, 'Информация о вакансии обновлена')
        else:
            messages.error(request, 'Проверьте правильность введенной информации!')
            return render(request, os.path.join('jobs', 'my_company', 'company_vacancy_edit.html'),
                          {'form': user_vacancy_form, 'pk': pk})
        return redirect(reverse('mycompany-vacancy-edit', kwargs={'pk': pk}))


class MyCompanyVacancyCreateView(LoginRequiredMixinOverride, HasCompanyRequiredMixin, View):
    def get(self, request):
        context = {'form': VacancyForm(), 'is_new_vacancy': True}
        return render(request, os.path.join('jobs', 'my_company', 'company_vacancy_edit.html'), context)

    def post(self, request):
        user_vacancy_form = VacancyForm(request.POST)
        if user_vacancy_form.is_valid():
            user_vacancy_instance = user_vacancy_form.save(commit=False)
            user_vacancy_instance.company = Company.objects.filter(owner=self.request.user).first()
            user_vacancy_instance.save()
            messages.info(self.request, 'Вакансия была создана')
        else:
            messages.error(request, 'Проверьте правильность введенной информации!')
            return render(request, os.path.join('jobs', 'my_company', 'company_vacancy_edit.html'),
                          {'form': user_vacancy_form, 'is_new_vacancy': True})
        return redirect(reverse('mycompany-vacancy-list'))


class MyCompanyVacancyDeleteView(LoginRequiredMixinOverride, View):
    def post(self, request, pk):
        Vacancy.objects.filter(id=pk).delete()
        messages.warning(request, 'Вакансия была удалена')
        return redirect(reverse('mycompany-vacancy-list'))


class MyCompanyFeedbackDeleteView(LoginRequiredMixinOverride, View):
    def post(self, request, id_vacancy, id_application):
        application = Application.objects.filter(id=id_application).first()
        if application:
            if application.vacancy.company.owner == request.user:
                username = application.written_username
                application.delete()
                messages.warning(request, f'Отклик от { username } был удалён')
            else:
                messages.error(request, 'У вас нет права на удаление выбранного отзыва!')
        else:
            messages.error(request, 'Отклик не был найден в базе данных')
        return redirect(reverse('mycompany-vacancy-edit', kwargs={'pk': id_vacancy}))
