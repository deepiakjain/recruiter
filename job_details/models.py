# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 25/07/2014

Recruiter project.

Model used for job detail filled by user can be admin or Recruiter
"""

from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.utils import IntegrityError

from account.models import JobSeeker, Recruiter
from account.constants import STATUS, JOB_STATUS, JOB_TYPE, INTEREST


class JobDetails(models.Model):
    recruiter = models.ForeignKey(Recruiter)
    job_title = models.CharField(max_length=30,blank=True,default=None)
    designation = models.CharField(max_length=30,blank=False)
    opening_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField(blank=True, null=True)
    number_of_positions = models.PositiveIntegerField(max_length=2, blank=False, default=1)
    job_opening_status = models.CharField(max_length=2, choices=JOB_STATUS, default='OP')
    country = models.CharField(max_length=30, blank=True)
    location_name = models.CharField(max_length=30, blank=True)
    min_experience = models.CharField(max_length=30, blank=True)
    max_experience = models.CharField(max_length=30, blank=True)
    skill_set = models.TextField(blank=True)
    roles_and_responsibilities = models.TextField(blank=True)
    job_type = models.CharField(max_length=2, choices=JOB_TYPE, default='PJ')
    job_code = models.CharField(max_length=70)  # Mostly we do search based on this unique code will create internally.

    def __unicode__(self):
        return "User %s from %s" % (self.recruiter.user.first_name, self.job_code)

    def applied_by_seeker(self, seeker):
        """
        Check status object exist for user and job.
        """
        return Status.objects.filter(job=self, seeker__user=seeker).exists()


class Status(models.Model):
    job = models.ManyToManyField(JobDetails)
    seeker = models.ManyToManyField(JobSeeker)
    status = models.CharField(max_length=2, choices=STATUS)


class InterestingResume(models.Model):
    recruiter = models.ManyToManyField(Recruiter)
    job = models.ManyToManyField(JobDetails)
    seeker = models.ManyToManyField(JobSeeker)
    interest = models.CharField(max_length=2, choices=INTEREST)

    def __unicode__(self):
        return "User: %s like profile: %s for job: %s" % (self.recruiter.user.username,
                                                  self.seeker.user.username, self.job.job_code)
