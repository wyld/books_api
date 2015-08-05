from django.conf.urls import patterns, url, include

from book_processing import views


urlpatterns = patterns('',
    url(r'^watermark/$', views.WatermarkBook.as_view(), name='watermark'),
)
