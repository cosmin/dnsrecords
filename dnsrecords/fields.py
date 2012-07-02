import re

from dnsrecords.fields_base import *

class IPv4Field(ReadPassThroughField):
    def __set__(self, obj, val):
        validate_ipv4(val)
        self.value = val

class HostNameField(ReadPassThroughField):
    def __set__(self, obj, val):
        validate_hostname(val)
        self.value = val

class HostNameOrIpField(ReadPassThroughField):
    def __set__(self, obj, val):
        if re.match("^[0-9.]+$", val):
            validate_ipv4(val)
        else:
            validate_hostname(val)

        self.value = val

class ServiceField(ReadPassThroughField):
    def __set__(self, obj, val):
        validate_label(val)
        self.value = val

class TextField(ReadPassThroughField):
    def __set__(self, obj, val):
        if type(val) == str or type(val) == unicode:
            self.value = val
        else:
            raise ValueError("Value is not string or unicode")
