from django import template

register = template.Library()

@register.filter
def service_icon(service_type):
    icons = {
        'wifi': 'fa-wifi',
        'breakfast': 'fa-utensils',
        'cleaning': 'fa-broom',
        'pool': 'fa-swimming-pool',
        'gym': 'fa-dumbbell',
        'spa': 'fa-spa',
        'transfer': 'fa-car',
    }
    return icons.get(service_type, 'fa-question-circle')