from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings


admin.autodiscover()


urlpatterns = patterns('',
    (r'^api/v1/books/', include('book_processing.urls', namespace='book_processing')),

    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
