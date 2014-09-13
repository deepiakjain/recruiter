# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 25/07/2014

Recruiter project.

Model used to for Recruiter profile or different type of role which may come later in the project.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator

# project constant
from account.constants import EXPERIENCE_CHOICES, YES_NO_CHOICES


class Qualification(models.Model):
    """
    """
    name = models.CharField(max_length=70, unique=True)

    def __unicode__(self):
        return self.name


class Technology(models.Model):
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


class JobSeeker(BaseProfile):
    profile_pic = models.ImageField(upload_to='user/profile', null=True)
    address = models.OneToOneField(Address, null=True)

    def __unicode__(self):
        return "User %s" %(self.user.first_name)

    def is_empty(self):
        return self.address is None

class SeekerCompanyInfo(models.Model):
    company_name = models.CharField(max_length=70, null=True)
    website = models.CharField(max_length=90, validators=[URLValidator()], null=True)
    joining_date = models.DateTimeField('Joining Date')
    notice_period = models.SmallIntegerField('Notice Period', null=True, help_text='in days only')
    current_ctc = models.CharField('Current CTC', max_length=30, help_text="Current salary in INR", null=True)
    job_change = models.CharField(max_length=1, choices=YES_NO_CHOICES, verbose_name="Looking for change")


class JobSeekerProfile(models.Model):
    seeker = models.OneToOneField(JobSeeker, null=True)
    current_company = models.OneToOneField(SeekerCompanyInfo, null=True)
    resume = models.FileField(upload_to='user/resume', null=True)
    profile_header = models.CharField(max_length=130,
                                      help_text="Shreeyansh Jain Python Developer", null=True)
    qualification = models.ForeignKey(Qualification, null=True)
    technology = models.ForeignKey(Technology, null=True)
    experience = models.CharField(max_length=2, choices=EXPERIENCE_CHOICES)
    expected_ctc = models.CharField(max_length=30, help_text="Expected salary in INR", null=True)
    current_loc = models.CharField(max_length=30, verbose_name="current location", null=True)
    relocate = models.CharField(max_length=1, choices=YES_NO_CHOICES, verbose_name="Ready to re-locate in India")
    free_time = models.DateTimeField(verbose_name="Good time to contact you")

    def __unicode__(self):
        return "User %s from %s" %(self.seeker.user.first_name, self.current_company.company_name)


# Recruiter Profile is always created by admin user on the request basis, show that
# application admin can manage him / her info
class RecruiterProfile(BaseProfile):
    company_email = models.EmailField(max_length=90, null=True)
    company = models.ForeignKey(CompanyProfile, null=True)

    def __unicode__(self):
        return "User %s from %s" % (self.user.first_name, self.company_name)
