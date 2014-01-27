import json
import hmac
import os
from urlparse import urlparse
from time import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from swiftclient import client
from hashlib import sha1
from datetime import datetime


@csrf_exempt
@require_POST
def create_slo(request, upload_to=''):
    slo = request.POST['slo']
    source_filename = request.POST['name']

    container = getattr(settings, 'DSD_SWIFT_CONTAINER', 'upload_container')
    swift_endpoint = getattr(settings, 'DSD_SWIFT_ENDPOINT', None)
    temp_url_key = getattr(settings, 'DSD_TEMP_URL_KEY', 'key')
    password = getattr(settings, 'DSD_PASSWORD', 'nomoresecrete')

    # We use swift credentials to get the account details

    username = getattr(settings, 'DSD_USERNAME', 'demo')
    tenant = getattr(settings, 'DSD_TENANT', 'demo')
    endpoint = getattr(settings, 'DSD_AUTH_ENDPOINT',
                       'http://localhost:5000/v2.0/')

    swift_connection = client.Connection(endpoint, username, password,
                                         tenant_name=tenant,
                                         auth_version="2.0")

    swift_connection.head_account()

    upload_to_strftime = datetime.now().strftime(upload_to).strip('/')
    file_path = os.path.normpath(os.path.join(upload_to_strftime,
                                         source_filename))

    r = swift_connection.put_object(container, file_path, slo,
                                    query_string='multipart-manifest=put')

    full_path = os.path.normpath(os.path.join(container, file_path))

    url = '%s/%s' % (swift_endpoint, full_path)
    r = {
        "file_url": url,
        "file_path": full_path
    }
    return HttpResponse(json.dumps(r), content_type="application/json")


@csrf_exempt
@require_POST
def get_upload_params(request, upload_to=''):
    source_filename = request.POST['name']
    data = create_upload_data(source_filename, upload_to)
    return HttpResponse(json.dumps(data), content_type="application/json")


def create_upload_data(source_filename, upload_to):

    container = getattr(settings, 'DSD_SWIFT_CONTAINER', 'upload_container')
    swift_endpoint = getattr(settings, 'DSD_SWIFT_ENDPOINT', None)
    temp_url_key = getattr(settings, 'DSD_TEMP_URL_KEY', 'key')
    password = getattr(settings, 'DSD_PASSWORD', 'nomoresecrete')

    if not swift_endpoint:
        # We use swift credentials to get the account details

        username = getattr(settings, 'DSD_USERNAME', 'demo')
        tenant = getattr(settings, 'DSD_TENANT', 'demo')
        endpoint = getattr(settings, 'DSD_AUTH_ENDPOINT',
                           'http://localhost:5000/v2.0/')

        swift_connection = client.Connection(endpoint, username, password,
                                             tenant_name=tenant,
                                             auth_version="2.0")

        swift_connection.head_account()
        swift_endpoint = swift_connection.url

    upload_to_strftime = datetime.now().strftime(upload_to).strip('/')
    path = os.path.normpath(os.path.join(container, upload_to_strftime,
                                         source_filename))

    url = '%s/%s' % (swift_endpoint, path)

    parsed = urlparse(url)
    method = 'PUT'
    expires = int(time() + 60)
    hmac_body = '%s\n%s\n%s' % (method, expires, parsed.path)
    sig = hmac.new(temp_url_key, hmac_body, sha1).hexdigest()

    temp_url = "%s?temp_url_sig=%s&temp_url_expires=%s" % (url, sig, expires)

    return {
        "temp_url": temp_url,
        "file_url": url,
        "file_path": path
    }

