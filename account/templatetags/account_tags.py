from django import template
register = template.Library()

@register.filter
def split(str, splitter):
    return str.split(splitter)[0]


@register.filter
def request_path(str):
    data = {'/': 'home'}
    return 'selected' if str.strip() in data else ''