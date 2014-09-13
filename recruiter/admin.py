# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from recruiter.forms import UserForm


class UserAdmin(UserAdmin):
    form = UserForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff',)
    search_fields = ('email',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)