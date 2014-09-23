# -*- coding: utf-8 -*-
import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from account.models import JobSeeker, SeekerExperienceInfo, Address,\
    EducationBackground, CompanyProfile, Recruiter


class InlineBaseProfileForm(forms.ModelForm):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    mobile_no = forms.CharField(label='Contact No.')
    profile_pic = forms.FileField(label='Display Picture', required=False)

    def __init__(self, *arg, **kwarg):
        self.empty_permitted = False
        super(InlineBaseProfileForm, self).__init__(*arg, **kwarg)

    def clean(self):
        cleaned_data = super(InlineBaseProfileForm, self).clean()
        return cleaned_data

    def clean_mobile_no(self):
        """
        Check its length is 10 digit and all are numbers no string
        """

        rule = re.compile(r'^(?:\+?91)?[0-9]\d{9,9}$')
        if not rule.search(str(self.cleaned_data['mobile_no'])):
            raise forms.ValidationError(_("Please enter valid mobile no."))
        return self.cleaned_data['mobile_no']

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class InlineAddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('street', 'city', 'country')

    def __init__(self, *arg, **kwarg):
        self.empty_permitted = False
        super(InlineAddressForm, self).__init__(*arg, **kwarg)

    def clean(self):
        cleaned_data = super(InlineAddressForm, self).clean()
        return cleaned_data


class InlineEducationBackgroundForm(forms.ModelForm):

    class Meta:
        model = EducationBackground


class InlineResumeForm(forms.ModelForm):

    class Meta:
        model = JobSeeker
        fields = ('resume',)


class InlineProfessionalDetailsForm(forms.ModelForm):

    class Meta:
        model = JobSeeker
        fields = ('expected_ctc_lac', 'expected_ctc_thousand', 'relocate')


class InlineSeekerDetailsForm(forms.ModelForm):

    class Meta:
        model = JobSeeker
        fields = ('profile_header', 'passport_number', 'preferred_loc', 'job_change', 'free_time',
                  'experience_yrs', 'experience_month', 'skill_set')


class InlineRecruiterDetailsForm(forms.ModelForm):

    class Meta:
        model = Recruiter
        fields = ('company_email',)
        exclude = ('company', )



class InlineCompanyProfileForm(forms.ModelForm):

    class Meta:
        model = CompanyProfile


class InlineSeekerCompanyForm(forms.ModelForm):
    class Meta:
        model = SeekerExperienceInfo
        exclude = ('company', )

