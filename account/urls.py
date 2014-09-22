from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from registration.backends.default.views import ActivationView

urlpatterns = patterns('',

    # account logout request
    url(r'^login/$', 'django.contrib.auth.views.login', {'extra_context': {'login_flag': True}}, name='auth_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='auth_logout'),

    #profile
    #url(r'^profile/$', 'account.views.profile_edit', name='profile'),
)

urlpatterns += patterns('',
            url(r'^profile/edit/$', 'account.views.profile_edit_wizard', name='profile_edit'),
            url(r'^profile/complete/$', 'account.views.profile_complete', name='profile_complete'),
    )

urlpatterns += patterns(
                        'account.registration_wizard',
                            url(r'^register/complete/$', 'registration_complete', name='registration_complete'),
                            url(r'^register/(?:(?P<step>[\w-]+)/)?$', 'registration_wizard',
                                name='registration_register'),
                        )

urlpatterns += patterns(
    '',
    url(r'^activate/complete/$',
        TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='registration_activate'),
)