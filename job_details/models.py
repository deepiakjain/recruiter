# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 25/07/2014

Recruiter project.

Model used for job detail filled by user can be admin or Recruiter
"""

from django.db import models
from account.models import JobSeeker, Recruiter

# Constants
STATUS = (
    ('AP', 'Applied'),
    ('AC', 'Accept'),
    ('NF', 'Not Fit'),
)


class JobDetails(models.Model):
    recruiter = models.ForeignKey(Recruiter)
    job_title = models.CharField(max_length=30,blank=True,default=None)
    designation = models.CharField(max_length=30,blank=False)
    opening_date = models.DateField()
    closing_date = models.DateField()
    number_of_positions = models.CharField(max_length=30,blank=False)
    job_opening_status = models.CharField(max_length=30,blank=False)
    country = models.CharField(max_length=30,blank=True,default=None)
    location_name = models.CharField(max_length=30,blank=True,default=None)
    min_experience = models.CharField(max_length=30,blank=True,default=None)
    max_experience = models.CharField(max_length=30,blank=True,default=None)
    skill_set = models.TextField(blank=True,default=None)
    roles_and_responsibilities = models.TextField(blank=True,default=None)
    job_type = models.CharField(max_length=30,blank=False)
    validity = models.CharField(max_length=30,blank=True,default=None)
    job_code = models.CharField(max_length=70)  # Mostly we do search based on this unique code will create internally.

    def __unicode__(self):
        return "User %s from %s" %(self.user.first_name, self.job_code)


class Status(models.Model):
    job = models.ManyToManyField(JobDetails)
    seeker = models.ManyToManyField(JobSeeker)
    status = models.CharField(max_length=2, choices=STATUS)