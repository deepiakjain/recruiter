# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 28/07/2014

Recruiter project.

Model reflection in django admin panel...
"""

# Register your models here.
from django.contrib import admin
from job_details.models import JobDetails, Status, InterestingResume


admin.site.register(JobDetails)
admin.site.register(Status)
admin.site.register(InterestingResume)