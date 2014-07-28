# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 25/07/2014

Recruiter project.

Model to keep user resumes at one place.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator


class Qualification(models.Model):
    """
    """
    name = models.CharField(max_length=70)


class JobDetails(models.Model):
    """
    """
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    father_name = models.CharField(max_length=70)
    qualification = models.ForeignKey(Qualification)
    resume = models.FileField(upload_to='user/resume')
    apply_date = models.DateTimeField('Apply date')
    job_code = models.CharField(max_length=70)  # user select pass after search.
    experience = models.PositiveIntegerField()

    def __unicode__(self):
        return "User %s father %s" % (self.first_name, self.father_name)
