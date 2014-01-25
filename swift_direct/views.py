import json
import hmac
import os
from urlparse import urlparse, urljoin
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
def get_upload_params(request, upload_to=''):
    source_filename = request.POST['name']
    data = create_upload_data(source_filename, upload_to)
    return HttpResponse(json.dumps(data), content_type="application/json")


def create_upload_data(source_filename, upload_to):
    username = settings.DSD_USERNAME
    key = settings.DSD_KEY
    tenant = settings.DSD_TENANT
    container = settings.DSD_CONTAINER_NAME
    endpoint = settings.DSD_AUTH_ENDPOINT

    swift_connection = client.Connection(endpoint, username, key,
                                         tenant_name=tenant,
                                         auth_version="2.0")

    swift_connection.head_account()
    key = 'key'
    upload_to_strftime = datetime.now().strftime(upload_to).strip('/')
    path = os.path.normpath(os.path.join(container, upload_to_strftime,
                                         source_filename))

    url = '%s/%s' % (swift_connection.url, path)

    parsed = urlparse(url)
    method = 'PUT'
    expires = int(time() + 60)
    hmac_body = '%s\n%s\n%s' % (method, expires, parsed.path)
    sig = hmac.new(key, hmac_body, sha1).hexdigest()

    temp_url = "%s?temp_url_sig=%s&temp_url_expires=%s" % (url, sig, expires)

    return {
        "temp_url": temp_url,
        "file_url": url
    }

