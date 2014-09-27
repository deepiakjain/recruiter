# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""

from account.models import JobSeeker, Recruiter
from account.constants import STATUS


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


def get_constant_dict(tuple_list):
    """
    Will convert list of tuples in tuple to dict.
    """
    return {key:value for value, key in tuple_list}