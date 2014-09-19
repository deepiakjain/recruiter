# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 28/07/2014

Recruiter project.

Model reflection in django admin panel...
"""

# Register your models here.
from django.contrib import admin
from account.models import Recruiter, JobSeeker, CompanyProfile, SeekerExperienceInfo, Address, EducationBackground

admin.site.register(Address)
admin.site.register(JobSeeker)
admin.site.register(CompanyProfile)
admin.site.register(SeekerExperienceInfo)
admin.site.register(Recruiter)
admin.site.register(EducationBackground)
