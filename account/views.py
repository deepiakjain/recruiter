# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""

# python imports
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect
from django.utils.decorators import classonlymethod
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .forms import (JobSeekerFormStep1, JobSeekerFormStep2,
                    JobSeekerFormStep3, JobSeekerFormStep4, RecruiterProfileForm)

from .models import JobSeeker, JobSeekerProfile


class ProfileEditWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=settings.TEMP_FOLDER)

    @classonlymethod
    def as_view(self, *args, **kwargs):
        form_list = (

            # seeker info
            ('seeker_profile', JobSeekerFormStep1),

            # seeker profile info
            ('seeker_advance_profile', JobSeekerFormStep2),
            ('seeker_expectation', JobSeekerFormStep3),
            ('seeker_company', JobSeekerFormStep4),

        )

        condition_dict = {
            'seeker_profile': ProfileEditWizard.seeker_condition,
            'seeker_advance_profile': ProfileEditWizard.advance_profile_condition,
            'seeker_expectation': ProfileEditWizard.expectation_condition,
            'seeker_company': ProfileEditWizard.seeker_company_condition,
        }

        return super(ProfileEditWizard, self).as_view(
            form_list=form_list,
            condition_dict=condition_dict,
            *args,
            **kwargs
        )

    @staticmethod
    def seeker_condition(wizard):
        return wizard.user_is_seeker() and wizard.profile_is_empty()

    @staticmethod
    def advance_profile_condition(wizard):
        return wizard.user_is_seeker() and wizard.profile_is_empty()

    @staticmethod
    def expectation_condition(wizard):
        return wizard.user_is_seeker() and wizard.profile_is_empty()

    @staticmethod
    def seeker_company_condition(wizard):
        return wizard.user_is_seeker() and wizard.profile_is_empty()

    def user_is_seeker(self):
        return JobSeeker.objects.filter(user=self.request.user).exists()

    def profile_is_empty(self):
        user = self.request.user
        role = None

        if self.user_is_seeker():
            role = JobSeeker.objects.get(user=user)

        return role is None or role.is_empty()

    def get_context_data(self, form, **kwargs):

        context = super(ProfileEditWizard, self).get_context_data(form=form, **kwargs)

        return context

    def get_form_kwargs(self, step=None):
        kwargs = {}
        return kwargs

    def get_template_names(self):
        name = 'accounts/profile_edit_wizard/%s.html' % self.steps.current
        return [name]

    def done(self, form_list, **kwargs):
        redirect_to = 'profile_edit'
        for form in form_list:
            if hasattr(form, 'save'):
                form.save()

                redirect_to = 'profile_complete'
        response = redirect(redirect_to)

        return response


def profile_complete(request):
    return render(request, 'accounts/profile_edit_wizard/configuration_completed.html')


profile_edit_wizard = ProfileEditWizard.as_view()
profile_edit_wizard = login_required(profile_edit_wizard)


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