from django.forms import Field
from swift_direct.widgets import SwiftDirect

__author__ = 'mm'


class SwiftDirectField(Field):

    def __init__(self, *args, **kwargs):
        upload_to = kwargs.pop('upload_to', '')
        self.widget = SwiftDirect(upload_to=upload_to)
        super(SwiftDirectField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)
        return super(SwiftDirectField, self).formfield(**defaults)
