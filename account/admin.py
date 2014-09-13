# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 28/07/2014

Recruiter project.

Model reflection in django admin panel...
"""

# Register your models here.
from django.contrib import admin
from account.models import JobSeekerProfile, RecruiterProfile, Qualification, Technology, JobSeeker,\
    CompanyProfile, SeekerCompanyInfo

admin.site.register(Qualification)
admin.site.register(Technology)
admin.site.register(JobSeeker)
admin.site.register(CompanyProfile)
admin.site.register(SeekerCompanyInfo)
admin.site.register(JobSeekerProfile)
admin.site.register(RecruiterProfile)
