# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""

from django.db.models.signals import class_prepared
from account.models import JobSeeker, Recruiter


def longer_username(sender, *args, **kwargs):
    # You can't just do `if sender == django.contrib.auth.models.User`
    # because you would have to import the model
    # You have to test using __name__ and __module__
    if sender.__name__ == "User" and sender.__module__ == "django.contrib.auth.models":
        sender._meta.get_field("username").max_length = 75

class_prepared.connect(longer_username)


class Profiles:
    PROFILE_NAMES = (
        ("seeker", JobSeeker),
        ("recruiter", Recruiter),
    )

    @classmethod
    def profile(cls, profile_code):
        return dict(cls.PROFILE_NAMES).get(profile_code)