import json
import logging
import re

from twilio.api import core

class OutgoingCallerIds(core.ListResource):
    """ A list of CallerId resources """

    def __init__(self, uri, **kwargs):
        name = "outgoing_caller_ids"
        uri += "/OutgoingCallerIds"
        super(OutgoingCallerIds, self).__init__(uri, name=name, **kwargs)

    def _load_instance(self, d):
        return OutgoingCallerId(self.uri, client=self.client, entries=d)

class OutgoingCallerId(core.InstanceResource):
    """ A Form resource """

    def __init__(self, uri, entries={}, **kwargs):
        if "sid" not in entries:
            raise core.TwilioException, "OutgoingCallerId sid missing"
        uri += "/" + entries["sid"]

        super(OutgoingCallerId, self).__init__(uri, entries=entries, **kwargs)


class AvailablePhoneNumbers(core.ListResource):
    """ A list of CallerId resources """

    def __init__(self, uri, **kwargs):
        name = "available_phone_numbers"
        uri += "/AvailablePhoneNumbers"
        super(AvailablePhoneNumbers, self).__init__(uri, name=name, **kwargs)

    def _load_instance(self, d):
        return AvailablePhoneNumber(self.uri, client=self.client, entries=d)

class AvailablePhoneNumber(core.InstanceResource):
    """ An available phone number resource """

    def __init__(self, uri, entries={}, **kwargs):
        super(AvailablePhoneNumber, self).__init__(uri, entries=entries, **kwargs)

class Calls(core.ListResource):
    """ A list of Call resources """

    def __init__(self, uri, **kwargs):
        name = "calls"
        uri += "/Calls"
        super(Calls, self).__init__(uri, name=name, **kwargs)

    def _load_instance(self, d):
        return Call(self.uri, client=self.client, entries=d)

class Call(core.InstanceResource):
    """ A call resource """

    def __init__(self, uri, entries={}, **kwargs):
        super(Call, self).__init__(uri, entries=entries, **kwargs)
