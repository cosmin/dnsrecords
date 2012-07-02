import re

def is_string(val):
    return type(val) == str or type(val) == unicode

def string_in_0_to_255(val):
    n = int(val)
    return 0 <= n <= 255

def satisfies_min(have, want):
    return want is None or have >= want

def satisfies_max(have, want):
    return want is None or have <= want

def is_numeric_only(val):
    return re.match("^[0-9]+$", val)

def validate_ipv4(val):
    if not is_string(val): raise ValueError("Value must be supplied as a string")
    components = val.split('.')
    if len(components) != 4 or not all(string_in_0_to_255(c) for c in components):
        raise ValueError("IPv4 address must be passed in as string of type x.y.z.w")

def validate_label(c):
    if not c:
        raise ValueError("Host name cannot be empty")
    if len(c) > 63:
        raise ValueError("Host name cannot be more than 63 characters")
    if is_numeric_only(c):
        raise ValueError("Host name cannot contain only numbers")
    if c.startswith("-") or c.endswith("-"):
        raise ValueError("Host name cannot start or end with dash '-'")
    if not re.match("^[0-9A-Za-z\-]+", c):
        raise ValueError("Host name can contain only a-z A-Z 0-9 and dash '-'")

def validate_hostname(val):
    if not is_string(val): raise ValueError("Value must be supplied as a string")

    components = val.split(".")
    if val.endswith("."):
        components = components[:-1]

    for c in components:
        validate_label(c)

class ReadPassThroughField(object):
    def __get__(self, obj, objtype):
        return self.value

class DefaultValueField(object):
    def __init__(self, default=None, **kw):
        if default is not None:
            self.value = default
        super(DefaultValueField, self).__init__(**kw)

class IntegerField(ReadPassThroughField, DefaultValueField):
    def __init__(self, signed=None, unsigned=None, **kw):
        super(IntegerField, self).__init__(**kw)
        if signed is not None:
            self.max = (2 ** (signed - 1)) - 1
        if unsigned is not None:
            self.max = (2 ** unsigned) - 1

    def __set__(self, obj, val):
        if 0 <= val <= self.max:
            self.value = val
        else:
            raise ValueError("Value %s out of range (max: %s)" % (val, self.max))

class ChoiceField(object):
    allowed = []

    def __init__(self, *allowed):
        self.allowed = allowed

    def __set__(self, obj, val):
        if val in self.allowed:
            self.value = val
        else:
            raise ValueError("Value %s is not in %s" % (val, self.allowed))
