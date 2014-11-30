from rest_framework import fields

class VirtualField(fields.Field):
    type_name = 'VirtualField'
    type_label = 'virtual'
    label = 'virtual'
    source = ''

    def __init__(self, value):
        self.value = value

    # def validate(self, value):
    #     pass

    def field_to_native(self, obj, field_name):
        return self.value

    def field_from_native(self, data, files, field_name, into):
        pass

    # def from_native(self, value):
    #     return value
