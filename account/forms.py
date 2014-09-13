# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""
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

# TODO: need to right save method


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