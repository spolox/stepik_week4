from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Specialty(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=20)
    picture = models.ImageField(
        upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR,
        height_field='picture_height_field',
        width_field='picture_width_field',
    )
    picture_height_field = models.PositiveIntegerField(default=0)
    picture_width_field = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.ImageField(
        upload_to=settings.MEDIA_COMPANY_IMAGE_DIR,
        height_field='logo_height_field',
        width_field='logo_width_field',
    )
    logo_height_field = models.PositiveIntegerField(default=0)
    logo_width_field = models.PositiveIntegerField(default=0)
    description = models.TextField()
    employee_count = models.CharField(max_length=100)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=100)
    written_phone = PhoneNumberField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return self.written_username + ' ' + self.written_phone


class Resume(models.Model):
    class WorkStatusChoices(models.TextChoices):
        NOT_IN_SEARCH = 'not_in_search', _('Не ищу работу')
        CONSIDERATION = 'consideration', _('Рассматриваю предложения')
        IN_SEARCH = 'in_search', _('Ищу работу')

    class SpecialtyChoices(models.TextChoices):
        FRONTEND = 'frontend', _('Фронтенд')
        BACKEND = 'backend', _('Бэкенд')
        GAMEDEV = 'gamedev', _('Геймдев')
        DEVOPD = 'devops', _('Девопс')
        DESIGN = 'design', _('Дизайн')
        PRODUCTS = 'products', _('Продукты')
        MANAGEMENT = 'management', _('Менеджмент')
        TESTING = 'testing', _('Тестирование')

    class GradeChoices(models.TextChoices):
        INTERN = 'intern', _('Стажёр')
        JUNIOR = 'junior', _('Джуниор')
        MIDDLE = 'middle', _('Мидл')
        SENIOR = 'senior', _('Синьор')
        LEAD = 'lead', _('Лид')

    class EducationChoices(models.TextChoices):
        MISSING = 'missing', _('Отсутствует')
        SECONDARY = 'secondary', _('Среднее')
        VOCATIONAL = 'vocational', _('Средне-специальное')
        INCOMPLETE_HIGHER = 'incomplete_higher', _('Неполное высшее')
        HIGHER = 'higher', _('Высшее')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    status = models.CharField(
        max_length=16,
        choices=WorkStatusChoices.choices,
        default=WorkStatusChoices.IN_SEARCH,
    )
    salary = models.IntegerField()
    specialty = models.CharField(
        max_length=16,
        choices=SpecialtyChoices.choices,
        default=SpecialtyChoices.FRONTEND,
    )
    grade = models.CharField(
        max_length=16,
        choices=GradeChoices.choices,
        default=GradeChoices.JUNIOR,
    )
    education = models.CharField(
        max_length=18,
        choices=EducationChoices.choices,
        default=EducationChoices.INCOMPLETE_HIGHER,
    )
    experience = models.TextField()
    portfolio = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return 'Resume of ' + self.name + ' ' + self.surname
