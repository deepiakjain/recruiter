# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 25/07/2014

Recruiter project.

Model used for job detail filled by user can be admin or Recruiter
"""

from django.db import models
from django.contrib.auth.models import User
from account.models import JobSeekerProfile

# Constants
STATUS = (
    ('AP', 'Applied'),
    ('AC', 'Accept'),
    ('NF', 'Not Fit'),
)


class Position(models.Model):
    """
    Position which are pre populated or maintain by admin only.
    """
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return "%s" % self.name


class Technology(models.Model):
    """
    technology supports
    """
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return "%s" % self.name


class JobDetails(models.Model):
    user = models.ForeignKey(User)
    position = models.ForeignKey(Position, related_name="positions")
    technology = models.ForeignKey(Technology, related_name="technologies")
    experience_required = models.CharField(max_length=10)
    description = models.TextField()
    create_date = models.DateTimeField('Job creation date')
    close_date = models.DateTimeField('Job close date', null=True, blank=True)
    job_code = models.CharField(max_length=70)  # Mostly we do search based on this unique code will create internally.

    def __unicode__(self):
        return "User %s from %s" %(self.user.first_name, self.job_code)


class Status(models.Model):
    job = models.ManyToManyField(JobDetails)
    seeker = models.ManyToManyField(JobSeekerProfile)
    status = models.CharField(max_length=2, choices=STATUS)