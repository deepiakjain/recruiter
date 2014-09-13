from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    # account logout request
    url(r'^login/$', 'django.contrib.auth.views.login', {'extra_context': {'login_flag': True}}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^', include('registration.backends.default.urls')),

    #profile
    url(r'^profile/$', 'account.views.profile_edit', name='profile'),
)

urlpatterns += patterns('',
            url(r'^profile/edit/$', 'account.views.profile_edit_wizard', name='profile_edit'),
            url(r'^profile/complete/$', 'account.views.profile_complete', name='profile_complete'),
    )