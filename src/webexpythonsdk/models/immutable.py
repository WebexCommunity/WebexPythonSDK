"""Model Webex JSON objects as native Python objects.

Classes:
    ImmutableData: Models Webex JSON objects as native Python objects.

The ImmutableData class models any JSON object passed to it as a string or
Python dictionary as a native Python object; providing attribute access using
native dot-syntax (`object.attribute`).

Copyright (c) 2016-2024 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
from collections import defaultdict

from webexpythonsdk.utils import json_dict
from .mixins.access_token import AccessTokenBasicPropertiesMixin
from .mixins.admin_audit_event import (
    AdminAuditEventBasicPropertiesMixin,
    AdminAuditEventDataBasicPropertiesMixin,
)
from .mixins.attachment_action import AttachmentActionBasicPropertiesMixin
from .mixins.event import EventBasicPropertiesMixin
from .mixins.guest_issuer_token import GuestIssuerTokenBasicPropertiesMixin
from .mixins.license import LicenseBasicPropertiesMixin
from .mixins.membership import MembershipBasicPropertiesMixin
from .mixins.message import MessageBasicPropertiesMixin
from .mixins.organization import OrganizationBasicPropertiesMixin
from .mixins.person import PersonBasicPropertiesMixin
from .mixins.role import RoleBasicPropertiesMixin
from .mixins.room import RoomBasicPropertiesMixin
from .mixins.room_tab import RoomTabBasicPropertiesMixin
from .mixins.room_meeting_info import RoomMeetingInfoBasicPropertiesMixin
from .mixins.team import TeamBasicPropertiesMixin
from .mixins.team_membership import TeamMembershipBasicPropertiesMixin
from .mixins.webhook import WebhookBasicPropertiesMixin
from .mixins.webhook_event import WebhookEventBasicPropertiesMixin
from .mixins.recording import RecordingBasicPropertiesMixin
from .mixins.meetings import MeetingBasicPropertiesMixin
from .mixins.meeting_templates import MeetingTemplateBasicPropertiesMixin
from .mixins.meeting_invitees import MeetingInviteeBasicPropertiesMixin

from .mixins.meeting_registrants import MeetingRegistrantBasicPropertiesMixin


class ImmutableData(object):
    """Model a Webex JSON object as an immutable native Python object."""

    def __init__(self, json_data):
        """Init a new ImmutableData object from a dictionary or JSON string.

        Args:
            json_data(dict, str): Input JSON string or dictionary.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(ImmutableData, self).__init__()
        self._json_data = json_dict(json_data)

    def __getattr__(self, item):
        """Provide native attribute access to the JSON object attributes.

        This method is called when attempting to access a object attribute that
        hasn't been defined for the object.  For example trying to access
        object.attribute1 when attribute1 hasn't been defined.

        ImmutableData.__getattr__() checks the original JSON object to see if
        the attribute exists, and if it does, it returns the attribute's value
        from the original JSON object.  This provides native access to all of
        the JSON object's attributes.

        Args:
            item(str): Name of the Attribute being accessed.

        Raises:
            AttributeError:  If the JSON object does not contain the attribute
                requested.

        """
        if item in list(self._json_data.keys()):
            item_data = self._json_data[item]
            if isinstance(item_data, dict):
                return ImmutableData(item_data)
            else:
                return item_data
        else:
            raise AttributeError(
                "'{}' object has no attribute '{}'" "".format(
                    self.__class__.__name__, item
                )
            )

    def __str__(self):
        """A human-readable string representation of this object."""
        class_str = self.__class__.__name__
        json_str = json.dumps(self._json_data, indent=2)
        return "Webex {}:\n{}".format(class_str, json_str)

    def __repr__(self):
        """A string representing this object as valid Python expression."""
        class_str = self.__class__.__name__
        json_str = json.dumps(self._json_data, ensure_ascii=False)
        return "{}({})".format(class_str, repr(json_str))

    @classmethod
    def _serialize(cls, data):
        """Serialize data to an frozen tuple."""
        if hasattr(data, "__hash__") and callable(data.__hash__):
            # If the data is already hashable (should be immutable) return it
            return data
        elif isinstance(data, list):
            # Freeze the elements of the list and return as a tuple
            return tuple((cls._serialize(item) for item in data))
        elif isinstance(data, dict):
            # Freeze the elements of the dictionary, sort them, and return
            # them as a list of tuples
            key_value_tuples = [
                (key, cls._serialize(value)) for key, value in data.items()
            ]
            key_value_tuples.sort()
            return tuple(key_value_tuples)
        else:
            raise TypeError(
                "Unable to freeze {} data type.".format(type(data))
            )

    def _freeze(self):
        """Freeze this object's JSON data."""
        return self._serialize(self._json_data)

    def __eq__(self, other):
        """Determine if two objects are equal."""
        return (
            isinstance(other, self.__class__)
            and self._freeze() == other._freeze()
        )

    def __hash__(self):
        """Hash the data object."""
        return hash(self._freeze())

    @property
    def json_data(self):
        """A copy of the data object's JSON data (OrderedDict)."""
        # TODO: When we move to Python v3+ only; use MappingProxyType.
        return self._json_data.copy()

    def to_dict(self):
        """Convert the Webex object data to a dictionary."""
        return dict(self._json_data)

    def to_json(self, **kwargs):
        """Convert the Webex object data to JSON.

        Any keyword arguments provided are passed through the Python JSON
        encoder.

        """
        return json.dumps(self._json_data, **kwargs)


class AccessToken(ImmutableData, AccessTokenBasicPropertiesMixin):
    """Webex Access-Token data model."""


class AdminAuditEventData(
    ImmutableData, AdminAuditEventDataBasicPropertiesMixin
):
    """Webex Admin Audit Event Data object data model."""


class AdminAuditEvent(ImmutableData, AdminAuditEventBasicPropertiesMixin):
    """Webex Admin Audit Event data model."""

    @property
    def data(self):
        """The event resource data."""
        return AdminAuditEventData(self._json_data.get("data"))


class AttachmentAction(ImmutableData, AttachmentActionBasicPropertiesMixin):
    """Webex Attachment Actions data model"""


class Event(ImmutableData, EventBasicPropertiesMixin):
    """Webex Event data model."""

    @property
    def data(self):
        """The event's data representation.

        This object will contain the event's resource, such as memberships or
        messages, at the time the event took place.
        """
        return ImmutableData(self._json_data.get("data"))


class License(ImmutableData, LicenseBasicPropertiesMixin):
    """Webex License data model."""


class Membership(ImmutableData, MembershipBasicPropertiesMixin):
    """Webex Membership data model."""


class Message(ImmutableData, MessageBasicPropertiesMixin):
    """Webex Message data model."""


class Organization(ImmutableData, OrganizationBasicPropertiesMixin):
    """Webex Organization data model."""


class Person(ImmutableData, PersonBasicPropertiesMixin):
    """Webex Person data model."""


class Role(ImmutableData, RoleBasicPropertiesMixin):
    """Webex Role data model."""


class Room(ImmutableData, RoomBasicPropertiesMixin):
    """Webex Room data model."""


class RoomTab(ImmutableData, RoomTabBasicPropertiesMixin):
    """Webex Room Tab data model."""


class RoomMeetingInfo(ImmutableData, RoomMeetingInfoBasicPropertiesMixin):
    """Webex Room Meeting Info data model."""


class Team(ImmutableData, TeamBasicPropertiesMixin):
    """Webex Team data model."""


class TeamMembership(ImmutableData, TeamMembershipBasicPropertiesMixin):
    """Webex Team-Membership data model."""


class Webhook(ImmutableData, WebhookBasicPropertiesMixin):
    """Webex Webhook data model."""


class WebhookEvent(ImmutableData, WebhookEventBasicPropertiesMixin):
    """Webex Webhook-Events data model."""

    @property
    def data(self):
        """The event resource data."""
        return ImmutableData(self._json_data.get("data"))


class GuestIssuerToken(ImmutableData, GuestIssuerTokenBasicPropertiesMixin):
    """Webex Guest Issuer Token data model"""


class Recording(ImmutableData, RecordingBasicPropertiesMixin):
    """Webex Recording data model"""


class Meeting(ImmutableData, MeetingBasicPropertiesMixin):
    """Webex Meeting data model"""


class MeetingTemplate(ImmutableData, MeetingTemplateBasicPropertiesMixin):
    """Webex MeetingTemplate data model"""


class MeetingInvitee(ImmutableData, MeetingInviteeBasicPropertiesMixin):
    """Webex MeetingInvitee data model"""


class MeetingRegistrant(ImmutableData, MeetingRegistrantBasicPropertiesMixin):
    """Webex MeetingRegistrant data model"""


immutable_data_models = defaultdict(
    lambda: ImmutableData,
    access_token=AccessToken,
    admin_audit_event=AdminAuditEvent,
    attachment_action=AttachmentAction,
    event=Event,
    license=License,
    membership=Membership,
    message=Message,
    organization=Organization,
    person=Person,
    role=Role,
    room=Room,
    room_tab=RoomTab,
    room_meeting_info=RoomMeetingInfo,
    team=Team,
    team_membership=TeamMembership,
    webhook=Webhook,
    webhook_event=WebhookEvent,
    guest_issuer_token=GuestIssuerToken,
    recording=Recording,
    meeting=Meeting,
    meetingTemplate=MeetingTemplate,
    meetingInvitee=MeetingInvitee,
    meetingRegistrant=MeetingRegistrant,
)


def immutable_data_factory(model, json_data):
    """Factory function for creating ImmutableData objects.

    Args:
        model(str): The data model to use when creating the
            ImmutableData object (message, room, membership, etc.).
        json_data(str, dict): The JSON string or dictionary data with
            which to initialize the object.

    Returns:
        ImmutableData: The created ImmutableData object.

    Raises:
        TypeError: If the json_data parameter is not a JSON string or
            dictionary.

    """
    return immutable_data_models[model](json_data)
