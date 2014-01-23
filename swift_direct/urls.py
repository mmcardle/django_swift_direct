from django.conf.urls import patterns, url
from swift_direct.views import get_upload_params


urlpatterns = patterns('',
    # Examples:
    url(r'^upload_params/(?P<upload_to>.*)$', get_upload_params,
        name='get_upload_params'),
)