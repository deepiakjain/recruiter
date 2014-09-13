# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Project
from account.forms import JobSeekerProfileForm, RecruiterProfileForm


@login_required
def profile_edit(request):
    """
    based on login user get his profile
    """

    form = get_user_profile_form(request.user, request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()

    return render(request, 'accounts/profile_edit.html', {'form': form})


def get_user_profile_form(user, post_data, files):
    """
    Return user form
    """
    import ipdb; ipdb.set_trace()
    if getattr(user, 'jobseeker', None):
        user_proile = getattr(user, 'jobseeker')
        form = JobSeekerProfileForm(post_data, files, instance=user_proile)
    else:
        user_proile = getattr(user, 'recruiterprofile')
        form = RecruiterProfileForm(post_data, files, instance=user_proile)

    return form