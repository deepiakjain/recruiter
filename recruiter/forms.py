# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""

from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('email',)

    username = forms.EmailField(max_length=64,
                                help_text="The person's email address.")

    def clean_email(self):
        email = self.cleaned_data['username']
        return email