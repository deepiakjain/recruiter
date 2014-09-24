# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 04/08/2014

Recruiter project.

Url for job related functionality
"""

from django.conf.urls import patterns, url

urlpatterns = patterns('',

    # account logout request
    url(r'^creation/$', 'job_details.views.create_job', name='job-create'),
    url(r'^edit/(?P<job_code>\w+)$', 'job_details.views.create_job', name='job-edition'),
    url(r'^detail/(?P<job_code>\w+)/$', 'job_details.views.job_detail', name='job-detail'),
    url(r'^', 'job_details.views.job_list', name='job-list'),
    url(r'^upload-resume/$', 'job_details.views.upload_resume', name='upload-resume'),
)