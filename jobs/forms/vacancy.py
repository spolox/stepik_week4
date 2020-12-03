import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Button
from crispy_forms.bootstrap import Field, FormActions, Div
from django import forms

from jobs.models import Vacancy, Specialty


class VacancyForm(forms.ModelForm):
    title = forms.CharField(label='Название вакансии', max_length=100)
    title.widget.attrs.update({'class': 'form-control'})
    specialty = forms.ModelChoiceField(label='Специализация', queryset=Specialty.objects.all(), empty_label=None)
    specialty.widget.attrs.update({'class': 'form-control'})
    salary_min = forms.CharField(label='Зарплата от', max_length=100)
    salary_min.widget.attrs.update({'class': 'form-control'})
    salary_max = forms.CharField(label='Зарплата до', max_length=100)
    salary_max.widget.attrs.update({'class': 'form-control'})
    skills = forms.CharField(label='Требуемые навыки', widget=forms.Textarea)
    skills.widget.attrs.update({'class': 'form-control', 'rows': 3, 'cols': 10})
    description = forms.CharField(label='Описание вакансии', widget=forms.Textarea)
    description.widget.attrs.update({'class': 'form-control', 'rows': 8, 'cols': 10})

    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description']

    def __init__(self, *args, **kwargs):
        super(VacancyForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.form_class = 'pt-5'
        self.helper.use_custom_control = True
        self.helper.layout = Layout(
            Row(
                Div(
                    Field('title'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    Field('specialty'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    Field('salary_min'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    Field('salary_max'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    Field('skills'),
                    css_class='col-12',
                ),
                Div(
                    Field('description'),
                    css_class='col-12',
                ),
            ),
            Row(
                Div(
                    FormActions(Submit('submit', 'Сохранить', css_class='btn btn-info')),
                    css_class='col-6',
                ),
                Div(
                    Button('delete', 'Удалить', css_class='d-none', css_id='id_btn_delete'),
                    css_class='col-6',
                ),
            ),
        )

    def save(self, commit=True):
        vacancy = super(VacancyForm, self).save(commit=False)
        vacancy.published_at = datetime.date.today()
        if commit:
            vacancy.save()
        return vacancy
