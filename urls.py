# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from filebrowser.sites import site
import settings

from django.contrib import admin
admin.autodiscover()
handler500 = 'fewline.catalog.views.internal_error'

urlpatterns = patterns('',
    (r'^', include('fewline.catalog.urls')),
    (r'^admin/filebrowser/', include(site.urls)),
    (r'^cart/', include('fewline.cart.urls')),
    (r'^blog/', include('fewline.blog.urls')),
    (r'^myadmin/', include('fewline.myadmin.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns ('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
             { 'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += staticfiles_urlpatterns()