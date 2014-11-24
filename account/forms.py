# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""

from django import forms
from utils.form_container import FormContainer
from account.profile_forms import InlineAddressForm, InlineSeekerCompanyForm, InlineBaseProfileForm,\
    InlineEducationBackgroundForm, InlineResumeForm, InlineProfessionalDetailsForm, InlineCompanyProfileForm,\
    InlineRecruiterDetailsForm, InlineJobReferenceForm

from utils.utilities import get_profile
from account.constants import YEAR_EXPERIENCE
from files.models import UUIDFile


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

        profile = get_profile(self.user)

        address = getattr(profile, 'address') if profile and getattr(profile, 'address', None) else None

        instances = {'profile': self.user, 'address': address}
        kwargs['instance'] = instances[prefix]

        return kwargs

    def save(self, commit=True):

        user = self.user
        # update user first and last name
        profile_data = self.forms['profile'].cleaned_data
        user.first_name = profile_data['first_name']
        user.last_name = profile_data['last_name']

        user.save()

        address = self.forms['address'].save()

        # based based on login user
        if hasattr(user, 'jobseeker'):
            profile = getattr(user, 'jobseeker')
        else:
            profile = getattr(user, 'recruiter')

        profile.mobile_no = profile_data['mobile_no']
        profile.profile_pic = profile_data['profile_pic']
        profile.address = address

        profile.save()


class JobReferenceForm(FormContainer):
    seeker_info = InlineJobReferenceForm

    def __init__(self, user, **kwargs):
        """
        set user in object to get instance
        """
        self.user = user
        super(JobReferenceForm, self).__init__(**kwargs)

    def get_form_kwargs(self, prefix, **kwargs):

        instances = {'seeker_info': self.user.jobseeker}

        kwargs['instance'] = instances[prefix]

        return kwargs


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

    def save(self, commit=True):
        seeker = self.user.jobseeker
        # save company data first
        qualification = self.forms['qualification'].save()

        # update seeker
        seeker.qualification = qualification

        seeker.save()


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

        extra_info = getattr(self.user.jobseeker, 'company_experience', None)
        company = getattr(self.user.jobseeker.company_experience, 'company', None) if extra_info else None

        instances = {'company': company,
                     'extra_info': extra_info
                     }

        kwargs['instance'] = instances[prefix]

        return kwargs

    def save(self, commit=True):

        # map with seeker profile
        seeker = self.user.jobseeker

        # save company data first
        company = self.forms['company'].save()

        # save extra info
        extra_info = self.forms['extra_info'].save()
        extra_info.company = company
        extra_info.save()

        seeker.company_experience = extra_info
        seeker.save()


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


class RecruiterDetailsForm(FormContainer):
    recruiter_info = InlineRecruiterDetailsForm
    company = InlineCompanyProfileForm
    company_address = InlineAddressForm

    def __init__(self, user, **kwargs):
        """
        set user in object to get instance
        """
        self.user = user
        super(RecruiterDetailsForm, self).__init__(**kwargs)

    def get_form_kwargs(self, prefix, **kwargs):

        recruiter = self.user.recruiter
        company = getattr(recruiter, 'company', None)
        company_address = getattr(company, 'address', None) if company else None

        instances = {'company': company,
                     'recruiter_info': recruiter,
                     'company_address': company_address,
                     }

        kwargs['instance'] = instances[prefix]

        return kwargs

    def save(self, commit=True):

        # map with seeker profile
        recruiter = self.user.recruiter

        # save company data first
        company = self.forms['company'].save()
        company_address = self.forms['company_address'].save()

        company.address = company_address
        company.save()

        recruiter.company = company
        recruiter.save()


class Search(forms.Form):
    search = forms.CharField(max_length=100, required=False)
    location = forms.CharField(max_length=100, required=False)
    experience = forms.ChoiceField(choices=YEAR_EXPERIENCE)