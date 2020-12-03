import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Button
from crispy_forms.bootstrap import Field, FormActions, Div
from django import forms
from django.forms.widgets import ClearableFileInput

from jobs.models import Company


class CustomClearableFileInput(ClearableFileInput):
    template_name = os.path.join('widgets', 'load_image.html')


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label='Название компании', label_suffix='', max_length=100)
    name.widget.attrs.update({'class': 'form-control'})
    employee_count = forms.CharField(label='Количество человек в компании', label_suffix='', max_length=100)
    employee_count.widget.attrs.update({'class': 'form-control'})
    location = forms.CharField(label='География', label_suffix='', max_length=100)
    location.widget.attrs.update({'class': 'form-control'})
    description = forms.CharField(label='Информация о компании', label_suffix='', widget=forms.Textarea)
    description.widget.attrs.update({'class': 'form-control', 'rows': 5, 'cols': 10})
    logo = forms.ImageField(label='Логотип', label_suffix='', widget=CustomClearableFileInput)

    class Meta:
        model = Company
        fields = ['name', 'location', 'logo', 'description', 'employee_count']

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.form_class = 'pt-5'
        self.helper.use_custom_control = True
        self.helper.layout = Layout(
            Row(
                Div(
                    Field('name'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    HTML('{{ form.logo.label_tag }}'
                         '{{ form.logo }}'
                         '<div class="text-danger list-inline-item"><strong>{{ form.logo.errors }}</strong></div>'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    Field('employee_count'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    Field('location'),
                    css_class='col-12 col-md-6',
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
