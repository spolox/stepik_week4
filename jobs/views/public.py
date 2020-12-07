import os

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from jobs.forms.application import ApplicationForm
from jobs.models import Vacancy, Specialty, Company
from jobs.views.override import LoginRequiredMixinOverride


def custom_handler404(request, exception):
    return HttpResponseNotFound('Извините, страница не найдена.')


def custom_handler500(request):
    return HttpResponseNotFound('Внутреняя ошибка сервака. Приносим свои извинения, повторите попытку позже')


class MainView(View):
    def get(self, request):
        context = {
            'companies': Company.objects.all().prefetch_related('vacancies'),
            'specialties': Specialty.objects.all().prefetch_related('vacancies'),
            'search_examples': settings.SEARCH_EXAMPLES,
        }
        return render(request, os.path.join('jobs', 'public', 'index.html'), context)


class ListVacancyView(ListView):
    model = Vacancy
    template_name = os.path.join('jobs', 'public', 'vacancy_list.html')
    queryset = model.objects.all().select_related('company')


class DetailVacancyView(DetailView):
    model = Vacancy
    template_name = os.path.join('jobs', 'public', 'vacancy_detail.html')

    def get_context_data(self, **kwargs):
        context = super(DetailVacancyView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = ApplicationForm(self.kwargs['pk'])
        return context

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs['pk']).select_related('company')


class ListSpecialtyView(DetailView):
    model = Specialty
    template_name = os.path.join('jobs', 'public', 'specialty_detail.html')

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs['pk']).prefetch_related('vacancies__company')


class DetailCompanyView(DetailView):
    model = Company
    template_name = os.path.join('jobs', 'public', 'company_detail.html')

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs['pk']).prefetch_related('vacancies__specialty')


class SendResumeView(LoginRequiredMixinOverride, View):
    def get(self, request, pk):
        return render(request, os.path.join('jobs', 'public', 'sent.html'), {'pk': pk})

    def post(self, request, pk):
        application_form = ApplicationForm(pk, request.POST)
        vacancy = Vacancy.objects.filter(id=pk).first()
        if application_form.is_valid():
            application_instance = application_form.save(commit=False)
            application_instance.user = request.user
            application_instance.vacancy = vacancy
            application_instance.save()
        else:
            return render(request, os.path.join('jobs', 'public', 'vacancy_detail.html'),
                          {'form': application_form, 'pk': pk, 'vacancy': vacancy})
        return render(request, os.path.join('jobs', 'public', 'sent.html'), {'pk': pk, 'send_success': True})


class SearchVacancyView(View):
    def get(self, request):
        query = request.GET.get('query', None)
        if not query:
            context = {'vacancy_list': Vacancy.objects.all().select_related('company')}
        else:
            query_search_vacancy = Vacancy.objects.filter(
                Q(title__icontains=query) |
                Q(skills__icontains=query) |
                Q(description__icontains=query)).all().select_related('company')
            context = {'vacancy_list': query_search_vacancy, 'query': query}
        return render(request, os.path.join('jobs', 'public', 'vacancy_list.html'), context)
