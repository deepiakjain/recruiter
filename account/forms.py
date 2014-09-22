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
    InlineEducationBackgroundForm, InlineResumeForm, InlineProfessionalDetailsForm, InlineCompanyProfileForm,\
    InlineSeekerDetailsForm


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
        profile_data = self.forms['profile'].cleaned_data
        user.first_name = profile_data['first_name']
        user.last_name = profile_data['last_name']

        user.save()

        address = self.forms['address'].save()

        # based based on login user
        if getattr(user, 'jobseeker'):
            profile = getattr(user, 'jobseeker')
        elif getattr(user, 'recruiter'):
            profile = getattr(user, 'recruiter')

        profile.mobile_no = profile_data['mobile_no']
        profile.profile_pic = profile_data['profile_pic']
        profile.address = address

        profile.save()


class SeekerDetailsForm(FormContainer):
    seeker_info = InlineSeekerDetailsForm

    def __init__(self, user, **kwargs):
        """
        set user in object to get instance
        """
        self.user = user
        super(SeekerDetailsForm, self).__init__(**kwargs)

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
        # if getattr(self.user.jobseeker, 'current_company'):
        #     company = getattr(self.user.jobseeker, 'current_company')

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