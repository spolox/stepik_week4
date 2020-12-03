from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag()
def get_variable():
    context = {
        'modal_title': 'Удаление компании',
        'modal_message': 'Вы уверены, что хотите удалить компанию? Потом его нельзя будет восстановить',
        'modal_url_action': reverse('mycompany-delete'),
    }
    return context
