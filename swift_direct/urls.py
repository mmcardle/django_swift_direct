from django.conf.urls import patterns, url
from swift_direct.views import get_upload_params, create_slo


urlpatterns = patterns('',
    url(r'^upload_params/(?P<upload_to>.*)$', get_upload_params,
        name='get_upload_params'),
    url(r'^upload_slo/(?P<upload_to>.*)$', create_slo,
        name='create_slo'),
)