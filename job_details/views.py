# -*- coding: utf-8 -*-
"""
Author : Shreeyansh Jain, 04/08/2014

Recruiter project.

Url for job related functionality
"""

from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

# project imports
from utils.utilities import user_is_recruiter
from job_details.models import JobDetails
from job_details.forms import JobDetailsForm


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
        form = JobDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))  # change with job detail page.
    else:
        initial = {'recruiter': user.recruiter}
        form = JobDetailsForm(instance=job_obj, initial=initial)

    template = 'jobs/job_detail_form.html'

    context = {'form': form}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))