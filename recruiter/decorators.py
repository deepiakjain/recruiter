from functools import wraps

from django.utils.decorators import available_attrs


def force_profile(view_func):
    """
    mark views with force_profile to complete profile before viewing it.
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.force_profile = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
