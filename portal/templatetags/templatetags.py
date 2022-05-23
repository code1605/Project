from django import template
register = template.Library()


@register.filter(name='sentiment')
def sentiment(value):
    return value *100

@register.filter(name='count')
def count(value):
    return len(value)