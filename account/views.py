# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 13/09/2014

Recruiter project.
"""

# python imports
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.utils.decorators import classonlymethod
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.conf import settings

from .forms import (ContactDetailsForm, EducationDetailsForm, ProfessionalDetailsForm,
                    RecruiterDetailsForm, JobReferenceForm)

from account.models import JobSeeker, Recruiter
from recruiter.decorators import force_profile
from job_details.models import InterestingResume

from utils.utilities import user_is_seeker, user_is_recruiter, get_profile
from .forms import Search


class ProfileEditWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=settings.TEMP_FOLDER)

    @classonlymethod
    def as_view(self, *args, **kwargs):
        form_list = (  # Will be common for both seeker and recruiter
                    ('contact_details', ContactDetailsForm),

                    ('education_details', EducationDetailsForm),
                    ('job_reference', JobReferenceForm),
                    ('professional_details', ProfessionalDetailsForm),

                    ('recruiter_details', RecruiterDetailsForm),
                    )

        condition_dict = {  # It should be common for both type user
                            'contact_details': ProfileEditWizard.contact_condition,

                            'education_details': ProfileEditWizard.seeker_profile_condition,
                            'job_reference': ProfileEditWizard.seeker_profile_condition,
                            'professional_details': ProfileEditWizard.seeker_profile_condition,

                            # recruiter profile
                            'recruiter_details': ProfileEditWizard.recruiter_profile_condition,
                         }

        return super(ProfileEditWizard, self).as_view(
            form_list=form_list,
            condition_dict=condition_dict,
            *args,
            **kwargs
        )

    @staticmethod
    def contact_condition(wizard):
        return wizard.profile_is_empty() or True

    @staticmethod
    def seeker_profile_condition(wizard):
        return user_is_seeker(wizard.request.user)

    @staticmethod
    def recruiter_profile_condition(wizard):
        return user_is_recruiter(wizard.request.user)

    def profile_is_empty(self):
        role = get_profile(self.request.user)
        return role is None or role.is_empty()

    def get_context_data(self, form, **kwargs):

        context = super(ProfileEditWizard, self).get_context_data(form=form, **kwargs)

        # add context user type
        context.update({'is_seeker': user_is_seeker(self.request.user)})

        if self.steps.current in ['job_expectations']:
            form.initial = self.get_cleaned_data_for_step(self.get_prev_step())

        return context

    def get_form_kwargs(self, step=None):
        kwargs = {}
        user = self.request.user
        kwargs['user'] = user
        return kwargs

    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        if step == 'contact_details':
            profile = get_profile(self.request.user)
            initial.update({'mobile_no': profile.mobile_no,
                            'profile_pic': profile.profile_pic})

        return initial

    def get_form_instance(self, step):
        instance = get_profile(self.request.user)

        return instance

    def get_template_names(self):
        name = 'accounts/profile_edit_wizard/%s.html' % self.steps.current
        return [name]

    def done(self, form_list, **kwargs):
        redirect_to = 'profile_edit'
        for form in form_list:
            if hasattr(form, 'save'):
                form.save()

                redirect_to = 'profile_complete'
        response = redirect(redirect_to)

        return response


@login_required()
def profile_complete(request):

    template = 'accounts/profile_edit_wizard/configuration_completed.html'
    context = {'is_seeker': user_is_seeker(request.user)}

    return render_to_response(template, context,
                              context_instance=RequestContext(request))

profile_edit_wizard = ProfileEditWizard.as_view()
profile_edit_wizard = login_required(profile_edit_wizard)


@force_profile
@login_required
def user_profile(request):
    """
    profile which will identify login user, display its data.
    identify if profile is empty the redirect to respective edit page.

    :param request:
    :return:
    """
    profile = get_profile(request.user)

    # check user is seeker or recruiter
    is_seeker = user_is_seeker(request.user)
    template = 'accounts/profile/user_profile.html'

    return render_to_response(template, {'profile': profile, 'is_seeker': is_seeker},
                              context_instance=RequestContext(request))


def recruiter_list(request):
    """
    Will list all jobs based on created or open date.
    """

    recruiters = Recruiter.objects.all().exclude(mobile_no=None).\
        exclude(user__username=request.user.username).order_by('user__first_name')

    template = 'accounts/user_list.html'
    context = {'users': recruiters, 'is_seeker': False}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@login_required()
@force_profile
def seeker_details(request, profile_id):
    """
    Will display seeker information
    """

    seeker = get_object_or_404(JobSeeker, id=profile_id)

    is_recruiter = user_is_recruiter(request.user) if not request.user.is_anonymous() else False

    #check InterestingResume info for the seeker
    interest = False
    if is_recruiter:
        interest = InterestingResume.objects.filter(seeker=seeker, recruiter=request.user.recruiter)

    template = 'accounts/profile/seeker_details.html'
    context = {'form': Search(), 'users': seeker,
               'profile_id': profile_id, 'interest': interest,
               'is_recruiter': is_recruiter}
    # based on is_recruiter value will show one button to express interest in the use
    # user profile.

    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def recruiter_details(request, profile_id):
    """
    Will list all jobs based on created or open date.
    """

    recruiter = get_object_or_404(Recruiter, id=profile_id)

    template = 'accounts/recruiter_details.html'
    context = {'users': recruiter}

    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@force_profile
def seeker_list(request):

    context = {'form': Search(), 'is_seeker': True}
    template = 'accounts/user_list.html'

    results = JobSeeker.objects.all().exclude(mobile_no=None).\
        exclude(resume=None).exclude(user__username=request.user.username)\
        .order_by('user__first_name')

    if request.method == 'POST':

        search = request.POST.get('search', None)
        if search:
            results = results.filter(Q(skill_set__icontains=search)|Q(qualification__qualification__icontains=search))

        experience = request.POST.get('experience', None)
        if experience:
            results = results.filter(experience_yrs__gte=experience)

        location = request.POST.get('location', None)
        if location:
            results = results.filter(preferred_loc__icontains=location)

        context.update({'form': Search(request.POST)})

    # pagination code for jobs
    paginator = Paginator(results, settings.ITEM_PER_PAGE)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    context.update({'users': users})
    return render_to_response(template, context,
                              context_instance=RequestContext(request))