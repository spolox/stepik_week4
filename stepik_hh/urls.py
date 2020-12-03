"""stepik_hh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path
from django.views.generic.base import RedirectView

from jobs.views.account import MyLoginView, MyRegisterView, MyProfileView, MyPasswordChangeView
from jobs.views.my_company import MyCompanyView, MyCompanyVacancyView, MyCompanyDeleteView, MyCompanyCreateView
from jobs.views.my_company import MyCompanyVacancyListView, MyCompanyVacancyDeleteView, MyCompanyVacancyCreateView
from jobs.views.my_company import MyCompanyFeedbackDeleteView
from jobs.views.my_resume import MyResumeView, MyResumeCreateView, MyResumeDeleteView, MyResumePublicView
from jobs.views.public import MainView, ListVacancyView, DetailVacancyView, ListSpecialtyView, DetailCompanyView
from jobs.views.public import SendResumeView
from jobs.views.public import SearchVacancyView
from jobs.views.public import custom_handler404, custom_handler500

#handler404 = custom_handler404
#handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/media/static/images/favicon.ico', permanent=True)),

    path('', MainView.as_view(), name='main'),
    path('companies/<int:pk>', DetailCompanyView.as_view(), name='company-detail'),
    path('vacancies/', ListVacancyView.as_view(), name='vacancy-list'),
    path('vacancies/<int:pk>', DetailVacancyView.as_view(), name='vacancy-detail'),
    path('vacancies/cat/<str:pk>', ListSpecialtyView.as_view(), name='specialty-list'),
    path('vacancies/<int:pk>/send', SendResumeView.as_view(), name='application-send'),
    path('mycompany/vacancies/<int:id_vacancy>/<int:id_application>/delete',
         MyCompanyFeedbackDeleteView.as_view(),
         name='application-delete',
         ),

    path('mycompany/', MyCompanyView.as_view(), name='mycompany'),
    path('mycompany/create', MyCompanyCreateView.as_view(), name='mycompany-create'),
    path('mycompany/delete', MyCompanyDeleteView.as_view(), name='mycompany-delete'),
    path('mycompany/vacancies/', MyCompanyVacancyListView.as_view(), name='mycompany-vacancy-list'),
    path('mycompany/vacancies/<int:pk>', MyCompanyVacancyView.as_view(), name='mycompany-vacancy-edit'),
    path('mycompany/vacancies/create', MyCompanyVacancyCreateView.as_view(), name='mycompany-vacancy-create'),
    path('mycompany/vacancies/<int:pk>/delete', MyCompanyVacancyDeleteView.as_view(), name='mycompany-vacancy-delete'),

    path('myresume/', MyResumeView.as_view(), name='myresume'),
    path('myresume/create', MyResumeCreateView.as_view(), name='myresume-create'),
    path('myresume/delete', MyResumeDeleteView.as_view(), name='myresume-delete'),
    path('resume/<int:pk>', MyResumePublicView.as_view(), name='resume-public'),

    path('myprofile/', MyProfileView.as_view(), name='myprofile'),

    path('register/', MyRegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/', MyPasswordChangeView.as_view(), name='change-password'),

    re_path(r'^search(?:(?P<query>\w+))?', SearchVacancyView.as_view(), name='search-vacancy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
