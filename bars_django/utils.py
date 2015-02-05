from rest_framework import fields

class VirtualField(fields.ReadOnlyField):
    type_name = 'VirtualField'
    type_label = 'virtual'
    label = 'virtual'
    source = ''

    def __init__(self, value):
        super(VirtualField, self).__init__()
        self.value = value

    def get_attribute(self, instance):
        return ''

    def to_representation(self, attr):
        return self.value
