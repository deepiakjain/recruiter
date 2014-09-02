# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 28/07/2014

Recruiter project.

Model reflection in django admin panel...
"""

# Register your models here.
from django.contrib import admin
from account.models import JobSeekerProfile, RecruiterProfile, Qualification

admin.site.register(Qualification)
admin.site.register(JobSeekerProfile)
admin.site.register(RecruiterProfile)
