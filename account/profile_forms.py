# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from account.models import JobSeekerProfile, SeekerCompanyInfo


class InlineUserForm(forms.ModelForm):

    def __init__(self, *arg, **kwarg):
        self.empty_permitted = False
        super(InlineUserForm, self).__init__(*arg, **kwarg)

    # def clean(self):
    #     cleaned_data = super(InlineUserForm, self).clean()
    #     return cleaned_data

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class InlineJobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('expected_ctc', 'current_loc', 'relocate', 'free_time',
                  'profile_header', 'technology', 'experience', 'resume')


class InlineSeekerCompanyForm(forms.ModelForm):
    class Meta:
        model = SeekerCompanyInfo

    def __init__(self, **kwargs):
        """
        set user in object to get instance
        """
        super(InlineSeekerCompanyForm, self).__init__(**kwargs)

    def save(self, commit=True):

        saved = super(InlineSeekerCompanyForm, self).save()

        seeker = JobSeekerProfile.objects.get(seeker=self.user.jobseeker)
        seeker.current_company = saved

        seeker.save()