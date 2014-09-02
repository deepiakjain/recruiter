from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # account logout request
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('account.urls')),

)

# flat pages info urls
urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^$', 'flatpage', {'url': '/home/'}, name='home'),
    url(r'^about-us/$', 'flatpage', {'url': '/about-us/'}, name='about'),
    url(r'^license/$', 'flatpage', {'url': '/license/'}, name='license'),
)