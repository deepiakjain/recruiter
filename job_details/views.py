# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 04/08/2014

Recruiter project.

Url for job related functionality
"""

import json

from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# project imports
from account.models import JobSeeker
from account.forms import Search
from account.profile_forms import InlineResumeForm

from job_details.models import JobDetails, Status, InterestingResume
from job_details.forms import JobDetailsForm

from utils.utilities import user_is_recruiter, user_is_seeker
from recruiter.decorators import force_profile


# TODO: need to work on it
@login_required()
@force_profile
def upload_resume(request):
    """
    This function first check login if not navigate to login page.
    2. navigate to upload resume page of respective user.
    3. delete older copy and store newer one in that place.
    """

    # get login user and verify it as will
    user = request.user

    # check is recruiter or not
    if user_is_recruiter(user):
        # redirect with message don't have access to perform this operation.
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = InlineResumeForm(request.POST, request.FILES, instance=user.jobseeker)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))
    else:
        form = InlineResumeForm(instance=user.jobseeker)

    template = 'accounts/profile/seeker_resume_form.html'

    context = {'form': form}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@login_required()
@force_profile
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
    url = reverse('job-create') if not job_code else reverse('job-edition', args=(job_code,))

    context = {'form': form, 'url': url}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))

@force_profile
def job_list(request):

    is_anonymous = request.user.is_anonymous()
    is_seeker = is_recruiter = False

    if not is_anonymous:
        is_seeker = user_is_seeker(request.user)
        is_recruiter = user_is_recruiter(request.user)

    context = {'form': Search(), 'is_seeker': is_seeker, 'is_recruiter': is_recruiter}
    template = 'jobs/jobs_list.html'

    results = JobDetails.objects.filter(job_opening_status='OP').order_by('-opening_date')

    # show only those jobs which create by recruiter else filter out for logged out user
    if not is_anonymous and not is_seeker:
        results = results.filter(recruiter__user=request.user)

    if request.method == 'POST':
        search = request.POST.get('search', None)
        if search:
            results = results.filter(Q(skill_set__icontains=search) | Q(roles_and_responsibilities__icontains=search)
                                     | Q(job_title__icontains=search))

        experience = request.POST.get('experience', None)
        if experience:
            results = results.filter(min_experience__gte=experience)

        location = request.POST.get('location', None)
        if location:
            results = results.filter(location_name__icontains=location)

        context.update({'form': Search(request.POST)})

    # update results for following function
    for result in results:
        result.applied = result.applied_by_seeker(request.user) if is_seeker else False
        if result.applied:
            #need to get correct name of status
            result.status = result.status_set.get(seeker__user=request.user).status

    # pagination code for jobs
    paginator = Paginator(results, settings.ITEM_PER_PAGE)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        jobs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        jobs = paginator.page(paginator.num_pages)

    context.update({'jobs': jobs, 'user': request.user})

    return render_to_response(template, context,
                              context_instance=RequestContext(request))

@force_profile
def job_detail(request, job_code):
    """
    Job detail which will display two all users
    """
    job = get_object_or_404(JobDetails, job_code=job_code)

    # check for logged in user
    is_anonymous = request.user.is_anonymous()
    is_seeker = is_recruiter = False
    context = {}

    if not is_anonymous:
        is_seeker = user_is_seeker(request.user)
        is_recruiter = user_is_recruiter(request.user)

    if is_seeker:
        job.applied = job.applied_by_seeker(request.user)

        if job.applied:
            #need to get correct name of status
            job.status = job.status_set.get(seeker__user=request.user).status

    elif is_recruiter:
        applied_status = Status.objects.filter(job=job)

        seekers = []
        for status in applied_status:
            seekers.append((status.seeker.all()[0], status.status))

        context.update({'seekers': seekers, 'is_recruiter': is_recruiter})

    template = 'jobs/job_detail.html'
    context.update({'job': job, 'is_seeker': is_seeker})
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@login_required()
@force_profile
def seeker_job_detail(request, job_code, seeker_id):
    job = get_object_or_404(JobDetails, job_code=job_code)
    seeker_obj = get_object_or_404(JobSeeker, id=seeker_id)

    is_recruiter = user_is_seeker(request.user)
    if not is_recruiter:
        return redirect(reverse('home'))

    template = 'jobs/job_detail.html'
    context = {'job': job, 'is_recruiter': is_recruiter, 'seeker_obj': seeker_obj}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@login_required()
@force_profile
def apply_for_job(request, job_code):
    """
    Apply for job this functionality is available only for seeker no for recruiter.
    """

    if user_is_recruiter(request.user):
        # redirect with message don't have access to perform this operation.
        return HttpResponse(json.dumps({'url': reverse('home')}), content_type="application/json")

    #check Status object exists or not.
    if Status.objects.filter(job__job_code=job_code, seeker=request.user.jobseeker):
        # redirect with message don't have access to perform this operation.
        return HttpResponse(json.dumps({'url': reverse('home')}), content_type="application/json")

    # get job object
    job_obj = get_object_or_404(JobDetails, job_code=job_code)

    status = Status(status='AP')
    status.save()

    # add many to many fields
    status.job.add(job_obj)
    status.seeker.add(request.user.jobseeker)

    return HttpResponse(json.dumps({'url': reverse('job-detail', args=[job_code])}), content_type="application/json")


@login_required()
@force_profile
def update_job_status(request, status, job_code, seeker_id):
    """
    Update job status by recruiter.
    """
    if user_is_seeker(request.user):
        # redirect with message don't have access to perform this operation.
        return HttpResponse(json.dumps({'url': reverse('home')}), content_type="application/json")

    # get status
    status_obj = get_object_or_404(Status, job__job_code=job_code, seeker__id=seeker_id)

    status_obj.status = status
    status_obj.save()

    return HttpResponse(json.dumps({'url': reverse('job-detail', args=[job_code])}), content_type="application/json")


@login_required()
@force_profile
def interesting_resume(request, seeker_id):
    """
    Show interest seeker resumes
    """
    if user_is_seeker(request.user):
        # redirect with message don't have access to perform this operation.
        return redirect(reverse('home'))

    # Get seeker info
    seeker_obj = JobSeeker.objects.get(id=seeker_id)

    # create entry in InterestingResume for the seeker
    interest = InterestingResume(interest='PM')
    interest.save()

    interest.seeker.add(seeker_obj)
    interest.recruiter.add(request.user.recruiter)

    return HttpResponse(json.dumps({'url': reverse('seeker-details', args=[seeker_id])}),
                        content_type="application/json")


@login_required()
@force_profile
def job_status(request):
    """
    """
    if user_is_seeker(request.user):
        # redirect with message don't have access to perform this operation.
        return redirect(reverse('home'))

    applied_jobs = Status.objects.filter(job__recruiter__user=request.user)

    context = {'job_status': applied_jobs}
    template = 'jobs/applied_jobs.html'

    return render_to_response(template, context,
                              context_instance=RequestContext(request))

@force_profile
def applied_job_list(request):
    if user_is_recruiter(request.user):
        # redirect with message don't have access to perform this operation.
        return redirect(reverse('home'))

    status = Status.objects.filter(seeker__user=request.user)

    context = {'job_status': status, 'is_seeker': True}
    template = 'jobs/applied_jobs.html'

    return render_to_response(template, context,
                              context_instance=RequestContext(request))

@login_required()
@force_profile
def close_job(request, job_code):
    """
    Close job as the position is filled..
    """

    if user_is_seeker(request.user):
        # redirect with message don't have access to perform this operation.
        return HttpResponse(json.dumps({'url': reverse('home')}), content_type="application/json")

    # get job object
    job_obj = get_object_or_404(JobDetails, job_code=job_code)
    job_obj.job_opening_status = 'CL'
    job_obj.closing_date = datetime.now()

    job_obj.save()

    return HttpResponse(json.dumps({'url': reverse('job-list')}), content_type="application/json")