from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from registration.backends.default.views import ActivationView

# search forms for candidate and jobs
from account.forms import Search

urlpatterns = patterns('',

                       # account logout request
                       url(r'^login/$', 'django.contrib.auth.views.login',
                           {'extra_context': {'login_flag': True, 'search_form': Search()}}, name='auth_login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {'next_page': '/'}, name='auth_logout'),

                       #profile
                       url(r'^profile/$', 'account.views.user_profile', name='profile'),
                       url(r'^profile/edit/$', 'account.views.profile_edit_wizard', name='profile_edit'),
                       url(r'^profile/complete/$', 'account.views.profile_complete', name='profile_complete'),

                       # user list
                       url(r'^seekers/', 'account.views.seeker_list', name='seeker-list'),
                       url(r'^recruiters/', 'account.views.recruiter_list', name='recruiter-list'),

                       url(r'^seeker/(?P<profile_id>\d+)/', 'account.views.seeker_details', name='seeker-details'),
                       url(r'^recruiter/(?P<profile_id>\d+)/', 'account.views.recruiter_details',
                           name='recruiter-details'),

                       url(r'^activate/complete/$',
                           TemplateView.as_view(template_name='registration/activation_complete.html'),
                           name='registration_activation_complete'),

                       url(r'^activate/(?P<activation_key>\w+)/$',
                           ActivationView.as_view(), name='registration_activate'),

                       url(r'^upload-resume/$', 'job_details.views.upload_resume', name='upload-resume'),
                       )

urlpatterns += patterns('account.registration_wizard',
                        url(r'^register/complete/$', 'registration_complete', name='registration_complete'),
                        url(r'^register/(?:(?P<step>[\w-]+)/)?$', 'registration_wizard', name='registration_register'),
                        )