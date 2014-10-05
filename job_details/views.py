# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 04/08/2014

Recruiter project.

Url for job related functionality
"""

from django.db.models import Q
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

# project imports
from account.models import JobSeeker
from account.forms import Search
from account.constants import STATUS

from job_details.models import JobDetails, Status
from job_details.forms import JobDetailsForm, InterestingResumeForm

from utils.utilities import get_constant_dict, user_is_recruiter, user_is_seeker

# TODO: need to work on it
@login_required()
def upload_resume(request):
    """
    This function first check login if not navigate to login page.
    2. navigate to upload resume page of respective user.
    3. delete older copy and store newer one in that place.
    """
    return render


@login_required()
def create_job(request, job_code=None):
    """
    job detail form will manage jobs
    only access by recruiter user and no other user can create.
    """

    # get login user and verify it as will
    user = request.user

    # check is recruiter or not
    if not user_is_recruiter(user):
        # redirect with message don't have access to perform this operation.
        return redirect(reverse('home'))

    # get job object.
    try:
        job_obj = JobDetails.objects.get(job_code=job_code)
    except JobDetails.DoesNotExist:
        job_obj = None

    # check job created by login user or not else don't allow change it.
    if job_obj and job_obj.recruiter.user != user:
        # redirect with message don't have access to perform this operation, display job list details pages
        return redirect(reverse('home'))  # change with job list page.

    if request.method == 'POST':
        form = JobDetailsForm(request.POST, instance=job_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('job-list'))
    else:
        initial = {'recruiter': user.recruiter}
        form = JobDetailsForm(instance=job_obj, initial=initial)

    template = 'jobs/job_detail_form.html'

    context = {'form': form}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


# def job_list(request):
#     """
#     Will list all jobs based on created or open date.
#     """
#
#     jobs = JobDetails.objects.filter(job_opening_status='OP').order_by('-opening_date')
#
#     is_seeker = user_is_seeker(request.user) if not request.user.is_anonymous() else False
#
#     template = 'jobs/jobs_list.html'
#     context = {'jobs': jobs, 'is_seeker': is_seeker}
#     return render_to_response(template, context,
#                               context_instance=RequestContext(request))


def job_list(request):

    is_seeker = user_is_seeker(request.user) if not request.user.is_anonymous() else False

    context = {'form': Search(), 'is_seeker': is_seeker}
    template = 'jobs/jobs_list.html'

    results = JobDetails.objects.filter(job_opening_status='OP').order_by('-opening_date')

    if request.method == 'POST':
        search = request.POST.get('search', None)
        if search:
            results = results.filter(Q(skill_set__icontains=search)|Q(roles_and_responsibilities__icontains=search))

        experience = request.POST.get('experience', None)
        if experience:
            results = results.filter(min_experience__gte=experience)

        location = request.POST.get('location', None)
        if location:
            results = results.filter(location_name__icontains=location)

        context.update({'form': Search(request.POST)})

    context.update({'jobs': results})

    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def job_detail(request, job_code):
    """
    Job detail which will display two all users
    """
    job = get_object_or_404(JobDetails, job_code=job_code)

    is_seeker = user_is_seeker(request.user) if not request.user.is_anonymous() else False

    template = 'jobs/job_detail.html'
    context = {'job': job, 'is_seeker': is_seeker}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@login_required()
def seeker_job_detail(request, job_code, seeker_id):
    job = get_object_or_404(JobDetails, job_code=job_code)

    is_recruiter = user_is_seeker(request.user)

    template = 'jobs/job_detail.html'
    context = {'job': job, 'is_recruiter': is_recruiter, 'seeker_id': seeker_id}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@login_required()
def apply_for_job(request, job_code):
    """
    Apply for job this functionality is available only for seeker no for recruiter.
    """
    if user_is_recruiter(request.user):
        # redirect with message don't have access to perform this operation.
        return redirect(reverse('home'))

    #check Status object exists or not.
    if Status.objects.filter(job__job_code=job_code, seeker=request.user.jobseeker):
        # redirect with message don't have access to perform this operation.
        return redirect(reverse('home'))

    # get job object
    job_obj = get_object_or_404(JobDetails, job_code=job_code)

    status = Status(job=job_obj, seeker=request.user.jobseeker, status='AP')
    status.save()

    #TODO: need to change with ajax call.
    return redirect(reverse('home'))


@login_required()
def update_job_status(request, status, job_code, seeker_id):
    """
    Update job status by recruiter.
    """
    if user_is_seeker(request.user):
        # redirect with message don't have access to perform this operation.
        return redirect(reverse('home'))

    # get status
    status_obj = get_object_or_404(Status, job__job_code=job_code, seeker__id=seeker_id)

    status_obj.status = get_constant_dict(STATUS)[status]
    status_obj.save()

    #TODO: need to change with ajax call.
    return redirect(reverse('home'))


@login_required()
def interesting_resume(request, seeker_id):
    """
    """
    if user_is_seeker(request.user):
        # redirect with message don't have access to perform this operation.
        return redirect(reverse('home'))

    form = InterestingResumeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
    else:
        seeker_obj = JobSeeker.objects.get(id=seeker_id)
        initial = {'seeker': seeker_obj, 'recruiter': request.user.recruiter}
        form.initial = initial

    context = {'form': form}
    template = 'jobs/interesting_resume.html'

    return render_to_response(template, context,
                              context_instance=RequestContext(request))