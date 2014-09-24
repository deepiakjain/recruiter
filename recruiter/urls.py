from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # account logout request
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('account.urls')),
    url(r'^jobs/', include('job_details.urls')),
    url(r'^files/', include('files.urls')),

)

# flat pages info urls
urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^$', 'flatpage', {'url': '/home/'}, name='home'),
    url(r'^about-us/$', 'flatpage', {'url': '/about-us/'}, name='about'),
    url(r'^license/$', 'flatpage', {'url': '/license/'}, name='license'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROTECTED_FILES_ROOT, 'show_indexes': True}),
    )
