from django import template
from account.constants import JOB_STATUS, STATUS, JOB_TYPE

register = template.Library()


def get_constant_dict(tuple_list):
    """
    Will convert list of tuples in tuple to dict.
    """
    return {key : value for key, value in tuple_list}


@register.filter
def split(str, splitter):
    return str.split(splitter)[0]

@register.filter
def request_path(str):
    data = {'/': 'home'}
    return 'selected' if str.strip() in data else ''

@register.simple_tag
def get_job_status_by_code(status_code):
    return get_constant_dict(JOB_STATUS).get(status_code, None)

@register.simple_tag
def get_status_by_code(status_code):
    return get_constant_dict(STATUS).get(status_code, None)

@register.simple_tag
def get_job_type_by_code(status_code):
    return get_constant_dict(JOB_TYPE).get(status_code, None)