
from django.shortcuts import redirect
from utils.utilities import get_profile


class ForceProfileMiddleware(object):
    """
    This middleware forces redirection to profile edit page
    if user's profile is empty.
    """
    def process_view(self, request, callback, callback_args, callback_kwargs):

        user = request.user
        if hasattr(callback, 'force_profile'):
            # Only perform checks for authenticated users who are not allowed
            # to access administration interface.
            if user.is_authenticated() and not (user.is_superuser or user.is_staff):
                role = get_profile(user)

                # If the user has a profile and it's empty - redirect them
                # to profile edit page.
                if role.is_empty():
                    return redirect('profile_edit')