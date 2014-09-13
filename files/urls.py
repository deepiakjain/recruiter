from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('files.views',
                       url(r'^download/(?P<file_path>.*)/(?P<file_name>.*)/$', 'download_file', name='download_file'),
                       url(r'^download/(?P<file_uuid>.*)/$', 'download_uuid_file', name='download_uuid_file'),
                       )
