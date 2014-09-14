# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""
import re
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from account.models import JobSeekerProfile, RecruiterProfile, JobSeeker, SeekerCompanyInfo


class JobSeekerFormStep1(ModelForm):
    first_name = forms.CharField(max_length=30, label=_("First name"))
    last_name = forms.CharField(max_length=30, label=_("Last name"))

    class Meta:
        model = JobSeeker
        fields = ('first_name', 'last_name', 'profile_pic', 'mobile_no')

    def __init__(self, user, **kwargs):
        """
        set user in object to get instance
        """
        self.user = user
        super(JobSeekerFormStep1, self).__init__(**kwargs)

    def clean_mobile_no(self):
        """
        Check its length is 10 digit and all are numbers no string
        """

        rule = re.compile(r'^(?:\+?91)?[0-9]\d{9,9}$')
        if not rule.search(str(self.cleaned_data['mobile_no'])):
            raise forms.ValidationError(_("Please enter valid mobile no."))
        return self.cleaned_data['mobile_no']

    def save(self, commit=True):

        user = self.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        super(JobSeekerFormStep1, self).save()


class JobSeekerFormStep2(ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('profile_header', 'qualification', 'technology', 'experience')


class JobSeekerFormStep3(ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('expected_ctc', 'current_loc', 'relocate', 'free_time')


class JobSeekerFormStep4(ModelForm):
    class Meta:
        model = SeekerCompanyInfo
        fields = ('company_name', 'website', 'joining_date', 'notice_period', 'current_ctc', 'job_change')


class RecruiterProfileForm(ModelForm):
    class Meta:
        model = RecruiterProfile