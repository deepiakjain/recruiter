# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""

from account.models import JobSeeker, Recruiter


def user_is_seeker(user):
    """
    will return true if seeker else false.

    :param user: user instance

    :return: boolean
    """
    return JobSeeker.objects.filter(user=user).exists()


def user_is_recruiter(user):
    """
    will return true if recruiter else false.

    :param user: user instance

    :return: boolean
    """
    return Recruiter.objects.filter(user=user).exists()


def get_profile(user):
    """
    Will return respective user profile
    :return:
    """

    if user_is_seeker(user):
        profile = JobSeeker.objects.get(user=user)
    else:
        profile = Recruiter.objects.get(user=user)

    return profile