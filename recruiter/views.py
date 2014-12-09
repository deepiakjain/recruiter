
from django.db.models import Q
from django.shortcuts import render_to_response
from utils.utilities import user_is_seeker, user_is_recruiter, get_profile
from job_details.models import JobDetails, InterestingResume, Status

from django.template import RequestContext

def home(request):
    """
    :param request:
    :return:
    """
    # check for user role
    # if seeker then display its related info
    # else recruiter info related ...

    is_anonymous = request.user.is_anonymous()

    # template used for home page..
    template = 'home/base.html'
    context_data = {}

    # check user is seeker or recruiter
    if not is_anonymous and user_is_seeker(request.user):

        # get latest jobs posted by recruiter...
        applied_jobs = Status.objects.filter(seeker__user=request.user)[:3]

        # Interest shown to the resumes.
        profile = get_profile(request.user)
        results = JobDetails.objects.filter(job_opening_status='OP').order_by('-opening_date')

        filter_data = []
        for skill in profile.skill_set.split(','):
            row = results.filter(Q(skill_set__icontains=skill))
            filter_data.extend(row)

        # context for recruiter home page ...
        context_data = {'lastest_jobs': filter_data[:3], 'applied_jobs': applied_jobs}

        # template name
        template = 'home/seeker.html'

    elif not is_anonymous and user_is_recruiter(request.user):
        # get latest jobs posted by recruiter...
        jobs = JobDetails.objects.filter(recruiter__user=request.user).order_by('-opening_date')[:2]

        # Interest shown to the resumes.
        favorites = InterestingResume.objects.filter(recruiter__user=request.user)[:3]

        # context for recruiter home page ...
        context_data = {'jobs': jobs, 'favorites': favorites}

        # template name
        template = 'home/recruiter.html'

    else:
        profile = None

    return render_to_response(template, context_data, context_instance=RequestContext(request))