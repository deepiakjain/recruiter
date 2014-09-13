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
    name = models.CharField(max_length=70, unique=True)

    def __unicode__(self):
        return self.name


class Address(models.Model):
    street = models.CharField(max_length=70)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=10)

    def __unicode__(self):
        return "%s - %s" % (self.city, self.country)


class CompanyProfile(models.Model):
    name = models.CharField(max_length=70, null=True)
    website = models.CharField(max_length=90, validators=[URLValidator()], null=True)
    logo = models.ImageField(upload_to='logo/companies', null=True)
    address = models.OneToOneField(Address)

    def __unicode__(self):
        return self.name


class BaseProfile(models.Model):
    user = models.OneToOneField(User, editable=False)
    mobile_no = models.PositiveIntegerField(max_length=11, null=True)  # Put form validation.
    create_date = models.DateTimeField('Creation Date', auto_now_add=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return "User %s from %s" %(self.user.first_name)


class JobSeekerProfile(BaseProfile):
    resume = models.FileField(upload_to='user/resume', null=True)
    profile_header = models.CharField(max_length=130,
                                      help_text="Shreeyansh Jain Python Developer", null=True)
    qualification = models.ForeignKey(Qualification, null=True)

    def __unicode__(self):
        return "User %s from %s" %(self.user.first_name, self.profile_header)


# Recruiter Profile is always created by admin user on the request basis, show that
# application admin can manage him / her info
class RecruiterProfile(BaseProfile):
    company_email = models.EmailField(null=True)
    company = models.ForeignKey(CompanyProfile, null=True)


    def __unicode__(self):
        return "User %s from %s" % (self.user.first_name, self.company_name)
