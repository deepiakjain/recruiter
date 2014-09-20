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

from .forms import (ContactDetailsForm, EducationDetailsForm,
                    ProfessionalDetailsForm, JobExpectationsForm, RecruiterProfileForm,
                    SeekerProfileForm, SeekerDetailsForm)

from .models import JobSeeker, Recruiter


class ProfileEditWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=settings.TEMP_FOLDER)

    @classonlymethod
    def as_view(self, *args, **kwargs):
        form_list = (

            # Will be common for both seeker and recruiter
            ('contact_details', ContactDetailsForm),

            # seeker profile info
            ('seeker_details', SeekerDetailsForm),
            ('education_details', EducationDetailsForm),
            ('professional_details', ProfessionalDetailsForm),
            ('job_expectations', JobExpectationsForm),

            # profile edit
            ('profile_edit', SeekerProfileForm),
           )

        condition_dict = {
            # It should be common for both type user
            'contact_details': ProfileEditWizard.contact_condition,

            'seeker_details': ProfileEditWizard.seeker_profile_condition,
            'education_details': ProfileEditWizard.seeker_profile_condition,
            'professional_details': ProfileEditWizard.seeker_profile_condition,
            'job_expectations': ProfileEditWizard.seeker_profile_condition,

            'profile_edit': ProfileEditWizard.seeker_profile_condition,
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
        return wizard.user_is_seeker() and wizard.profile_is_empty()

    @staticmethod
    def recruiter_profile_condition(wizard):
        return wizard.user_is_recruiter() and wizard.profile_is_empty()

    def user_is_seeker(self):
        return JobSeeker.objects.filter(user=self.request.user).exists()

    def user_is_recruiter(self):
        return Recruiter.objects.filter(user=self.request.user).exists()

    def get_profile(self):
        user = self.request.user
        if self.user_is_seeker():
            profile = JobSeeker.objects.get(user=user)
        else:
            profile = Recruiter.objects.get(user=user)
        return profile

    def profile_is_empty(self):
        role = self.get_profile()
        return role is None or role.is_empty()

    def get_context_data(self, form, **kwargs):

        context = super(ProfileEditWizard, self).get_context_data(form=form, **kwargs)

        if self.steps.current in ['job_expectations', 'professional_details']:
            form.initial = self.get_cleaned_data_for_step(self.get_prev_step())

        return context

    def get_form_kwargs(self, step=None):
        kwargs = {}
        print self.steps.current

        user = self.request.user
        kwargs['user'] = user
        return kwargs

    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        if step == 'contact_details':
            profile = self.get_profile()
            initial.update({'mobile_no': profile.mobile_no,
                            'profile_pic': profile.profile_pic})

        return initial

    def get_form_instance(self, step):
        instance = self.instance_dict.get(step, None)
        if step == 'contact_details':
            instance = self.get_profile()

        return instance

    def get_template_names(self):
        name = 'accounts/profile_edit_wizard/%s.html' % self.steps.current
        return [name]

    def done(self, form_list, **kwargs):
        redirect_to = 'profile_edit'
        for form in form_list:
            if hasattr(form, 'save') and not isinstance(form, JobSeekerFormStep2):
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
    import ipdb; ipdb.set_trace()
    form = SeekerProfileForm(request.user)
    # form = get_user_profile_form(request.user, request.POST or None, request.FILES or None)

    if request.method == 'POST':
        import ipdb; ipdb.set_trace()
        if form.is_valid():
            form.save()

    return render(request, 'accounts/profile_edit.html', {'form': form})


def get_user_profile_form(user, post_data, files):
    """
    Return user form
    """

    if getattr(user, 'jobseeker', None):
        user_proile = getattr(user, 'jobseeker')
    else:
        user_proile = getattr(user, 'recruiter')
        form = RecruiterProfileForm(post_data, files, instance=user_proile)

    return form