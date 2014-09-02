from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    # account logout request
    url(r'^login/$', 'django.contrib.auth.views.login', {'extra_context': {'login_flag': True}}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^', include('registration.backends.default.urls')),

)