from dnsrecords.fields import *

class DnsRecord(object):
    name = HostNameField()
    ttl = IntegerField(signed=32)

class SOA(DnsRecord):
    primary = HostNameField()
    hostmaster = HostNameField()
    serial = IntegerField(unsigned=32)
    refresh = IntegerField(signed=32)
    retry = IntegerField(signed=32)
    expiry = IntegerField(signed=32)
    minimum = IntegerField(signed=32)

class A(DnsRecord):
    ip = IPv4Field()

class CNAME(DnsRecord):
    target = HostNameOrIpField()

class PTR(DnsRecord):
    target = HostNameField()

class MX(DnsRecord):
    priority = IntegerField(unsigned=16)
    target = HostNameOrIpField()

class TXT(DnsRecord):
    target = TextField()

class SPF(TXT): pass

class SRV(DnsRecord):
    service = ServiceField()
    protocol = ChoiceField('TCP', 'UDP')

    priority = IntegerField(unsigned=16)
    weight = IntegerField(unsigned=16)
    port = IntegerField(unsigned=16)

    target = HostNameOrIpField()
