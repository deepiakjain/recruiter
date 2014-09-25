# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""

# python imports
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect, render_to_response
from django.utils.decorators import classonlymethod
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

from .forms import (ContactDetailsForm, EducationDetailsForm, ProfessionalDetailsForm,
                    JobExpectationsForm, SeekerDetailsForm, RecruiterDetailsForm)

from account.models import JobSeeker, Recruiter

from utils.utilities import user_is_seeker, user_is_recruiter, get_profile


class ProfileEditWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=settings.TEMP_FOLDER)

    @classonlymethod
    def as_view(self, *args, **kwargs):
        form_list = (  # Will be common for both seeker and recruiter
                    ('contact_details', ContactDetailsForm),

                    ('seeker_details', SeekerDetailsForm),  # seeker profile info
                    ('education_details', EducationDetailsForm),
                    ('professional_details', ProfessionalDetailsForm),
                    ('job_expectations', JobExpectationsForm),
                    ('job_expectations', JobExpectationsForm),
                    ('recruiter_details', RecruiterDetailsForm),
                    )

        condition_dict = {  # It should be common for both type user
                            'contact_details': ProfileEditWizard.contact_condition,

                            'seeker_details': ProfileEditWizard.seeker_profile_condition,
                            'education_details': ProfileEditWizard.seeker_profile_condition,
                            'professional_details': ProfileEditWizard.seeker_profile_condition,
                            'job_expectations': ProfileEditWizard.seeker_profile_condition,

                            # recruiter profile
                            'recruiter_details': ProfileEditWizard.recruiter_profile_condition,
                         }

        return super(ProfileEditWizard, self).as_view(
            form_list=form_list,
            condition_dict=condition_dict,
            *args,
            **kwargs
        )

    @staticmethod
    def contact_condition(wizard):
        return wizard.profile_is_empty() or True

    @staticmethod
    def seeker_profile_condition(wizard):
        return user_is_seeker(wizard.request.user)

    @staticmethod
    def recruiter_profile_condition(wizard):
        return user_is_recruiter(wizard.request.user)

    def profile_is_empty(self):
        role = get_profile(self.request.user)
        return role is None or role.is_empty()

    def get_context_data(self, form, **kwargs):

        context = super(ProfileEditWizard, self).get_context_data(form=form, **kwargs)

        if self.steps.current in ['job_expectations']:
            form.initial = self.get_cleaned_data_for_step(self.get_prev_step())

        return context

    def get_form_kwargs(self, step=None):
        kwargs = {}
        user = self.request.user
        kwargs['user'] = user
        return kwargs

    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        if step == 'contact_details':
            profile = get_profile(self.request.user)
            initial.update({'mobile_no': profile.mobile_no,
                            'profile_pic': profile.profile_pic})

        return initial

    def get_form_instance(self, step):
        instance = get_profile(self.request.user)

        return instance

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


def user_profile(request):
    """
    profile which will identify login user, display its data.
    identify if profile is empty the redirect to respective edit page.

    :param request:
    :return:
    """
    profile = get_profile(request.user)

    if profile.is_empty():
        return redirect(reverse('profile_edit'))

    # check user is seeker or recruiter
    is_seeker = user_is_seeker(request.user)
    template = 'accounts/profile/user_profile.html'

    return render_to_response(template, {'profile': profile, 'is_seeker': is_seeker},
                              context_instance=RequestContext(request))


def seeker_list(request):
    """
    Will list all jobs based on created or open date.
    """

    seekers = JobSeeker.objects.all().exclude(mobile_no=None).\
        exclude(resume=None).exclude(user__username=request.user.username)\
        .order_by('user__first_name')

    template = 'accounts/user_list.html'
    context = {'users': seekers, 'is_seeker': True}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def recruiter_list(request):
    """
    Will list all jobs based on created or open date.
    """

    recruiters = Recruiter.objects.all().exclude(mobile_no=None).\
        exclude(user__username=request.user.username).order_by('user__first_name')

    template = 'accounts/user_list.html'
    context = {'users': recruiters, 'is_seeker': False}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))