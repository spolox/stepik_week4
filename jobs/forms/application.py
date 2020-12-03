from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import Field, FormActions, Div
from django import forms
from django.urls import reverse_lazy
from phonenumber_field.formfields import PhoneNumberField

from jobs.models import Application


class ApplicationForm(forms.ModelForm):
    written_username = forms.CharField(label='Вас зовут', max_length=100)
    written_phone = PhoneNumberField(label='Ваш телефон')
    written_cover_letter = forms.CharField(label='Сопроводительное письмо', max_length=100, widget=forms.Textarea)
    written_cover_letter.widget.attrs.update({'class': 'form-control', 'rows': 10, 'cols': 10})

    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']

    def __init__(self, pk, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('application-send', kwargs={'pk': pk})

        self.helper.form_class = 'card mt-4 mb-3'

        self.helper.layout = Layout(
            Div(
                Field('written_username'),
                Field('written_phone'),
                Field('written_cover_letter'),
                FormActions(Submit('submit', 'Записаться на пробный урок', css_class='btn btn-primary my-2')),
                css_class='card-body mx-3',
            ),
        )
