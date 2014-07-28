# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 28/07/2014

Recruiter project.

Model reflection in django admin panel...
"""

# Register your models here.
from django.contrib import admin
from job_details.models import Position, Technology, JobDetails

admin.site.register(Position)
admin.site.register(Technology)
admin.site.register(JobDetails)