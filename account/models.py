# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 25/07/2014

Recruiter project.

Model used to for Recruiter profile or different type of role which may come later in the project.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    company_name = models.CharField(max_length=70)
    website = models.TextField(validators=[URLValidator()])
    mobile_no = models.PositiveIntegerField(max_length=11)  # Put form validation.
    create_date = models.DateTimeField('Creation Date')

    def __unicode__(self):
        return "User %s from %s" %(self.user.first_name, self.company_name)