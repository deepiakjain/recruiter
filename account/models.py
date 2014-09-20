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
from account.constants import YEAR_EXPERIENCE, MONTH_EXPERIENCE, YES_NO_CHOICES, GENDER_CHOICES, CTC_RANGE


class Address(models.Model):
    street = models.TextField()
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=10)

    def __unicode__(self):
        return "%s - %s" % (self.city, self.country)


class CompanyProfile(models.Model):
    name = models.CharField(max_length=70, null=True)
    website = models.CharField(max_length=90, validators=[URLValidator()], null=True)
    logo = models.ImageField(upload_to='logo/companies', null=True, blank=True)
    address = models.OneToOneField(Address, null=True, blank=True)

    def __unicode__(self):
        return self.name


class SeekerExperienceInfo(models.Model):
    company = models.OneToOneField(CompanyProfile, related_name='company', null=True)
    joining_date = models.DateTimeField('Date of joining')
    notice_period = models.SmallIntegerField('Notice Period', null=True, help_text='in days only')
    current_ctc_lac = models.CharField(max_length=2, choices=CTC_RANGE)
    current_ctc_thousand = models.CharField(max_length=2, choices=CTC_RANGE)


class EducationBackground(models.Model):
    qualification = models.CharField(max_length=30, null=True)
    institute_name = models.CharField(max_length=40, null=True)
    year_of_passing = models.CharField(max_length=4, null=True)
    percentage = models.CharField(max_length=5, null=True)
    special_achievement = models.CharField(max_length=40, null=True, blank=True)

    def __unicode__(self):
        return "Complete %s from %s in year %s" %(self.qualification, self.institute_name, self.year_of_passing)


class BaseProfile(models.Model):
    user = models.OneToOneField(User, editable=True)
    create_date = models.DateTimeField('Creation Date', auto_now_add=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gender")
    mobile_no = models.PositiveIntegerField(max_length=11, null=True)  # Put form validation.
    profile_pic = models.ImageField(upload_to='user/profile', null=True, blank=True)
    address = models.OneToOneField(Address, null=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return "User %s from %s" %(self.user.first_name)


class JobSeeker(BaseProfile):

    #TODO: profile pic and resume should store at one folder named user.
    resume = models.FileField(upload_to='user/resume', null=True)
    passport_number = models.CharField(max_length=30, null=True, blank=True)
    profile_header = models.CharField(max_length=130, help_text="Python Developer", null=True)

    # Experience section
    experience_yrs = models.CharField(max_length=2, choices=YEAR_EXPERIENCE, default=0,
                                      help_text="experience in year")
    experience_month = models.CharField(max_length=2, choices=MONTH_EXPERIENCE, default=0,
                                        help_text="experience in month")
    company_experience = models.OneToOneField(SeekerExperienceInfo, related_name='companies', null=True)
    skill_set = models.TextField(null=True, help_text="Comma-separated technologies")

    # Education qualification can be multiple.
    qualification = models.ForeignKey(EducationBackground, null=True)

    # Expectation Section
    expected_ctc_lac = models.CharField(max_length=2, choices=CTC_RANGE, default=0)
    expected_ctc_thousand = models.CharField(max_length=2, choices=CTC_RANGE, default=0)
    relocate = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='Y',
                                verbose_name="Ready to re-locate in India")

    # time when recruiter can contact.
    free_time = models.TimeField(verbose_name="Good time to contact you", null=True)

    # preferred locations.
    preferred_loc = models.CharField(max_length=30, help_text="Comma-separated cities name")
    job_change = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='Y',
                                  verbose_name="Looking job for change")

    def __unicode__(self):
        return "User %s" % (self.user.first_name)

    def is_empty(self):
        return self.mobile_no is None


# Recruiter Profile is always created by admin user on the request basis, show that
# application admin can manage him / her info
class Recruiter(BaseProfile):
    company_email = models.EmailField(max_length=90, null=True)
    company = models.ForeignKey(CompanyProfile, null=True)

    def __unicode__(self):
        return "User %s from %s" % (self.user.first_name, self.company_name)
