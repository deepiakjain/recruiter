# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 25/07/2014

Recruiter project.

Model used for job detail filled by user can be admin or Recruiter
"""

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

# project imports
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

@receiver(post_save, sender=JobDetails)
def send_email_if_job_closed(sender, instance, **kwargs):
    """
    Send email if job was closed to update the owner and to keep recode of the jobs closed.
    """

    if instance.job_opening_status == 'CL':

        # get current site info
        site = Site.objects.get_current()
        touser = instance.recruiter.user.email

        ctx_dict = {'site': site, 'job_code':instance.job_code,
                    'username': touser.split('@')[0],
                    'job_title': instance.job_title}

        subject = render_to_string('jobs/emails/job_close_email_subject.txt',
                                   ctx_dict)

        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('jobs/emails/job_close_email.txt',
                                   ctx_dict)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [touser], fail_silently=False)


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
