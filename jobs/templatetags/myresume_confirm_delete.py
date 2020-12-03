from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag()
def get_variable():
    context = {
        'modal_title': 'Удаление резюме',
        'modal_message': 'Вы уверены, что хотите удалить резюме? Потом его нельзя будет восстановить',
        'modal_url_action': reverse('myresume-delete'),
    }
    return context
