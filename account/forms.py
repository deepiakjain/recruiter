# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""
import re
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from account.models import JobSeekerProfile, RecruiterProfile, JobSeeker, SeekerCompanyInfo
from utils.form_container import FormContainer
from account.profile_forms import InlineUserForm, InlineJobSeekerForm, InlineSeekerCompanyForm


class JobSeekerFormStep1(ModelForm):
    first_name = forms.CharField(max_length=30, label=_("First name"))
    last_name = forms.CharField(max_length=30, label=_("Last name"))

    class Meta:
        model = JobSeeker
        fields = ('first_name', 'last_name', 'profile_pic', 'mobile_no')

    def __init__(self, user, **kwargs):
        """
        set user in object to get instance
        """
        self.user = user
        super(JobSeekerFormStep1, self).__init__(**kwargs)

    def clean_mobile_no(self):
        """
        Check its length is 10 digit and all are numbers no string
        """

        rule = re.compile(r'^(?:\+?91)?[0-9]\d{9,9}$')
        if not rule.search(str(self.cleaned_data['mobile_no'])):
            raise forms.ValidationError(_("Please enter valid mobile no."))
        return self.cleaned_data['mobile_no']

    def save(self, commit=True):

        user = self.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        super(JobSeekerFormStep1, self).save()


class JobSeekerFormStep2(ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('profile_header', 'qualification', 'technology', 'experience', 'resume')
        exclude = ('seeker', )


class JobSeekerFormStep3(ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ('expected_ctc', 'current_loc', 'relocate', 'free_time',
                  'profile_header', 'qualification', 'technology', 'experience', 'seeker')

        widgets = {'profile_header': forms.HiddenInput(),
                   'qualification': forms.HiddenInput(),
                   'technology': forms.HiddenInput(),
                   'experience': forms.HiddenInput(),
                   'seeker': forms.HiddenInput(),
                   # 'resume': forms.HiddenInput(),
                   }


class JobSeekerFormStep4(ModelForm):
    class Meta:
        model = SeekerCompanyInfo

    def __init__(self, user, **kwargs):
        """
        set user in object to get instance
        """
        self.user = user
        super(JobSeekerFormStep4, self).__init__(**kwargs)

    def save(self, commit=True):

        saved = super(JobSeekerFormStep4, self).save()

        seeker = JobSeekerProfile.objects.get(seeker=self.user.jobseeker)
        seeker.current_company = saved

        seeker.save()


class SeekerProfileForm(FormContainer):

    user = InlineUserForm
    seeker = inlineformset_factory(User, JobSeeker, can_delete=False)
    seeker_profile = inlineformset_factory(JobSeeker, JobSeekerProfile, form=InlineJobSeekerForm,
                                           max_num=1, extra=1, can_delete=False)

    seeker_company = InlineSeekerCompanyForm

    def __init__(self, user, **kwargs):

        self.user = user
        super(SeekerProfileForm, self).__init__(**kwargs)

    def get_form_kwargs(self, prefix, **kwargs):

        company = None
        if getattr(self.user.jobseeker.seeker, 'current_company'):
            company = getattr(self.user.jobseeker.seeker, 'current_company')

        instances = {
            'user': self.user,
            'seeker': self.user,
            'seeker_profile': self.user.jobseeker,
            'seeker_company': company,
        }
        kwargs['instance'] = instances[prefix]

        return kwargs

    # def is_valid(self):
    #     import ipdb; ipdb.set_trace()
    #     flag = self.forms['user'].is_valid()

class RecruiterProfileForm(ModelForm):
    class Meta:
        model = RecruiterProfile