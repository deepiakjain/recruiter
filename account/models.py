# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 25/07/2014

Recruiter project.

Model used to for Recruiter profile or different type of role which may come later in the project.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator


class Qualification(models.Model):
    """
    """
    name = models.CharField(max_length=70)


class BaseProfile(models.Model):
    user = models.OneToOneField(User)
    mobile_no = models.PositiveIntegerField(max_length=11)  # Put form validation.
    create_date = models.DateTimeField('Creation Date')

    class Meta:
        abstract = True

    def __unicode__(self):
        return "User %s from %s" %(self.user.first_name, self.company_name)


class JobSeekerProfile(BaseProfile):
    resume = models.FileField(upload_to='user/resume')
    profile_header = models.CharField(max_length=130)
    qualification = models.ForeignKey(Qualification)


# Recruiter Profile is always created by admin user on the request basis, show that
# application admin can manage him / her info
class RecruiterProfile(BaseProfile):
    company_name = models.CharField(max_length=70)
    website = models.CharField(max_length=90, validators=[URLValidator()])