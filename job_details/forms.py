# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 24/09/2014

Recruiter project.
"""

from django import forms
from job_details.models import JobDetails


class JobDetailsForm(forms.ModelForm):
    class Meta:
        model = JobDetails
        exclude = ('job_code',)
        widgets = {'recruiter': forms.HiddenInput(), }

    def save(self, commit=True):
        """
        Create job code
        """
        job_detail = super(JobDetailsForm, self).save()

        if not getattr(job_detail, 'job_code', None):
            job_code = 'JC%s%s' % (job_detail.id, job_detail.recruiter.id)  # value of job id and recruiter id

            job_detail.job_code = job_code
            job_detail.save()