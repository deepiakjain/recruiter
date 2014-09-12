# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""

from django.forms import ModelForm
from account.models import JobSeekerProfile, RecruiterProfile


class JobSeekerProfileForm(ModelForm):

    class Meta:
        model = JobSeekerProfile


class RecruiterProfileForm(ModelForm):
    class Meta:
        model = RecruiterProfile