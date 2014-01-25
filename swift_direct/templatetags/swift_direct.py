from django import template
from uuid import uuid4
from django.core.urlresolvers import reverse
from django.forms import Media
from ..widgets import swift_direct_js as swift_direct_js_html
from ..widgets import swift_direct_css as swift_direct_css_html
register = template.Library()

__author__ = 'mm'


@register.inclusion_tag('swift_direct/swift_direct_widget.html')
def swift_direct(element_id=None, element_name='', filename='', upload_to=''):

    if not element_id:
        element_id = uuid4()

    param_url = reverse('get_upload_params', kwargs={'upload_to': upload_to})

    return {
        'param_url': param_url,
        'force_filename': filename,
        'filename': filename,
        'element_id': element_id,
        'element_name': element_name,
    }

@register.simple_tag()
def swift_direct_css():
    css = Media()
    css.add_css(swift_direct_css_html)
    return css


@register.simple_tag()
def swift_direct_js():
    js = Media()
    js.add_js(swift_direct_js_html)
    return js