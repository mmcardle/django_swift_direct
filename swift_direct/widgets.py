import os
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

__author__ = 'mm'

swift_direct_js = \
    (
        'swift_direct/jquery/jquery-1.10.2.min.js',
        'swift_direct/jQuery-File-Upload-9.5.2/js/vendor/jquery.ui.widget.js',
        'swift_direct/jQuery-File-Upload-9.5.2/js/jquery.iframe-transport.js',
        'swift_direct/jQuery-File-Upload-9.5.2/js/jquery.fileupload.js',
        'swift_direct/js/swift_direct.js',
    )

swift_direct_css = {
    'all': (
        'swift_direct/css/django_swift.css',
    )
}


class SwiftDirect(widgets.TextInput):

    class Media:
        js = swift_direct_js
        css = swift_direct_css

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        super(SwiftDirect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        element_id = final_attrs.get('id')
        kwargs = {'upload_to': self.upload_to}

        param_url = reverse('get_upload_params', kwargs=kwargs)
        file_url = value if value else ''
        file_name = os.path.basename(file_url)

        context = {
            'param_url': param_url,
            'file_url': file_url,
            'file_name': file_name,
            'element_id': element_id,
            'name': name
        }

        output = render_to_string('swift_direct/swift_direct_widget.html',
                                  dictionary=context)

        return mark_safe(output)