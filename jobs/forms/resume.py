from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Button
from crispy_forms.bootstrap import Field, FormActions, Div
from django import forms

from jobs.models import Resume


class ResumeForm(forms.ModelForm):
    name = forms.CharField(label='Имя', max_length=100)
    name.widget.attrs.update({'class': 'form-control'})
    surname = forms.CharField(label='Фамилия', max_length=100)
    surname.widget.attrs.update({'class': 'form-control'})
    status = forms.ChoiceField(label='Готовность к работе',
                               choices=Resume.WorkStatusChoices.choices,
                               initial=Resume.WorkStatusChoices.IN_SEARCH,
                               )
    status.widget.attrs.update({'class': 'form-control'})
    salary = forms.CharField(label='Ожидаемое вознаграждение', max_length=100)
    salary.widget.attrs.update({'class': 'form-control'})
    specialty = forms.ChoiceField(label='Специализация',
                                  choices=Resume.SpecialtyChoices.choices,
                                  initial=Resume.SpecialtyChoices.FRONTEND,
                                  )
    specialty.widget.attrs.update({'class': 'form-control'})
    grade = forms.ChoiceField(label='Квалификация',
                              choices=Resume.GradeChoices.choices,
                              initial=Resume.GradeChoices.JUNIOR,
                              )
    grade.widget.attrs.update({'class': 'form-control'})
    education = forms.ChoiceField(label='Образование',
                                  choices=Resume.EducationChoices.choices,
                                  initial=Resume.EducationChoices.HIGHER,
                                  )
    education.widget.attrs.update({'class': 'form-control'})
    experience = forms.CharField(label='Опыт работы', widget=forms.Textarea)
    experience.widget.attrs.update({'class': 'form-control', 'rows': 8, 'cols': 10})
    portfolio = forms.URLField(label='Ссылка на портфолио', required=False)
    portfolio.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Resume
        fields = ['name', 'surname', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio']

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)

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
                    Field('surname'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    Field('status'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    Field('salary'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    Field('specialty'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    Field('grade'),
                    css_class='col-12 col-md-6',
                ),
                Div(
                    Field('education'),
                    css_class='col-12',
                ),
                Div(
                    Field('experience'),
                    css_class='col-12',
                ),
                Div(
                    Field('portfolio'),
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
