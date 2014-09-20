# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from account.models import JobSeeker, Recruiter, SeekerExperienceInfo
from utils.form_container import FormContainer
from account.profile_forms import InlineAddressForm, InlineSeekerCompanyForm, InlineBaseProfileForm,\
    InlineEducationBackgroundForm, InlineResumeForm, InlineProfessionalDetailsForm, InlineCompanyProfileForm


class ContactDetailsForm(FormContainer):
    profile = InlineBaseProfileForm
    address = InlineAddressForm

    def __init__(self, user, **kwargs):
        """
        set user in object to get instance
        """
        self.user = user
        super(ContactDetailsForm, self).__init__(**kwargs)

    def get_form_kwargs(self, prefix, **kwargs):
        profile = None

        if getattr(self.user, 'jobseeker'):
            profile = getattr(self.user, 'jobseeker')
        elif getattr(self.user, 'recruiter'):
            profile = getattr(self.user, 'jobseeker')

        address = getattr(profile, 'address') if profile and getattr(profile, 'address') else None

        instances = {'profile': self.user, 'address': address}
        kwargs['instance'] = instances[prefix]

        return kwargs

    def save(self, commit=True):

        user = self.user
        # update user first and last name

        user.first_name = self.profile.cleaned_data['first_name']
        user.last_name = self.profile.cleaned_data['last_name']

        user.save()

        address = self.address.save()

        # based based on login user
        if getattr(user, 'jobseeker'):
            profile = getattr(user, 'jobseeker')
        elif getattr(user, 'recruiter'):
            profile = getattr(user, 'recruiter')

        profile.mobile_no = self.profile.cleaned_data['mobile_no']
        profile.profile_pic = self.profile.cleaned_data['profile_pic']
        profile.address = address

        profile.save()


class SeekerDetailsForm(ModelForm):
    class Meta:
        model = JobSeeker
        fields = ('profile_header', 'passport_number', 'preferred_loc', 'job_change', 'free_time',
                  'experience_yrs', 'experience_month', 'skill_set')

    def __init__(self, user, **kwargs):
        """
        set user in object to get instance
        """
        self.user = user
        super(SeekerDetailsForm, self).__init__(**kwargs)


class EducationDetailsForm(FormContainer):
    qualification = InlineEducationBackgroundForm
    resume_file = InlineResumeForm

    def __init__(self, user, **kwargs):
        """
        set user in object to get instance
        """
        self.user = user
        super(EducationDetailsForm, self).__init__(**kwargs)

    def get_form_kwargs(self, prefix, **kwargs):

        instances = {'qualification': self.user.jobseeker.qualification,
                     'resume_file': self.user.jobseeker
                     }

        kwargs['instance'] = instances[prefix]

        return kwargs


class ProfessionalDetailsForm(FormContainer):
    company = InlineCompanyProfileForm
    extra_info = InlineSeekerCompanyForm

    def __init__(self, user, **kwargs):
        """
        set user in object to get instance
        """
        self.user = user
        super(ProfessionalDetailsForm, self).__init__(**kwargs)

    def get_form_kwargs(self, prefix, **kwargs):

        company = getattr(self.user.jobseeker.company_experience, 'company', None)

        instances = {'profession': self.user.jobseeker,
                     'company': company,
                     'extra_info': self.user.jobseeker.company_experience
                     }

        kwargs['instance'] = instances[prefix]

        return kwargs


class JobExpectationsForm(FormContainer):
    profession = InlineProfessionalDetailsForm

    def __init__(self, user, **kwargs):
        """
        set user in object to get instance
        """
        self.user = user
        super(JobExpectationsForm, self).__init__(**kwargs)

    def get_form_kwargs(self, prefix, **kwargs):

        instances = {'profession': self.user.jobseeker}

        kwargs['instance'] = instances[prefix]

        return kwargs


class SeekerProfileForm(FormContainer):

    user = InlineBaseProfileForm
    seeker = inlineformset_factory(User, JobSeeker, can_delete=False)
    # seeker_profile = inlineformset_factory(SeekerExperienceInfo, JobSeeker, form=InlineJobSeekerForm,
    #                                        max_num=1, extra=1, can_delete=False)

    seeker_company = InlineSeekerCompanyForm

    def __init__(self, user, **kwargs):

        self.user = user
        super(SeekerProfileForm, self).__init__(**kwargs)

    def get_form_kwargs(self, prefix, **kwargs):

        company = None
        if getattr(self.user.jobseeker.seeker, 'current_company'):
            company = getattr(self.user.jobseeker.seeker, 'current_company')

        instances = {
            'user': self.user,
            'seeker': self.user,
            'seeker_profile': self.user.jobseeker,
            'seeker_company': company,
        }
        kwargs['instance'] = instances[prefix]

        return kwargs

    # def is_valid(self):
    #     import ipdb; ipdb.set_trace()
    #     flag = self.forms['user'].is_valid()

class RecruiterProfileForm(ModelForm):
    class Meta:
        model = Recruiter