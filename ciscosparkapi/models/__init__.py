# -*- coding: utf-8 -*-
"""Cisco Spark data models."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from collections import defaultdict

from .access_token import AccessTokenBasicPropertiesMixin
from .event import EventBasicPropertiesMixin
from .license import LicenseBasicPropertiesMixin
from .membership import MembershipBasicPropertiesMixin
from .message import MessageBasicPropertiesMixin
from .organization import OrganizationBasicPropertiesMixin
from .person import PersonBasicPropertiesMixin
from .role import RoleBasicPropertiesMixin
from .room import RoomBasicPropertiesMixin
from .simple import SimpleDataModel
from .sparkdata import SparkData
from .team import TeamBasicPropertiesMixin
from .team_membership import TeamMembershipBasicPropertiesMixin
from .webhook import WebhookBasicPropertiesMixin
from .webhook_event import WebhookEventBasicPropertiesMixin
from ..utils import json_dict


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


class AccessToken(SparkData, AccessTokenBasicPropertiesMixin):
    """Cisco Spark Access-Token data model."""


class Event(SparkData, EventBasicPropertiesMixin):
    """Cisco Spark Event data model."""


class License(SparkData, LicenseBasicPropertiesMixin):
    """Cisco Spark License data model."""


class Membership(SparkData, MembershipBasicPropertiesMixin):
    """Cisco Spark Membership data model."""


class Message(SparkData, MessageBasicPropertiesMixin):
    """Cisco Spark Message data model."""


class Organization(SparkData, OrganizationBasicPropertiesMixin):
    """Cisco Spark Organization data model."""


class Person(SparkData, PersonBasicPropertiesMixin):
    """Cisco Spark Person data model."""


class Role(SparkData, RoleBasicPropertiesMixin):
    """Cisco Spark Role data model."""


class Room(SparkData, RoomBasicPropertiesMixin):
    """Cisco Spark Room data model."""


class Team(SparkData, TeamBasicPropertiesMixin):
    """Cisco Spark Team data model."""


class TeamMembership(SparkData, TeamMembershipBasicPropertiesMixin):
    """Cisco Spark Team-Membership data model."""


class Webhook(SparkData, WebhookBasicPropertiesMixin):
    """Cisco Spark Webhook data model."""


class WebhookEvent(SparkData, WebhookEventBasicPropertiesMixin):
    """Cisco Spark Webhook-Events data model."""


spark_data_models = defaultdict(
    lambda: SparkData,
    access_token=AccessToken,
    event=Event,
    license=License,
    membership=Membership,
    message=Message,
    organization=Organization,
    person=Person,
    role=Role,
    room=Room,
    team=Team,
    team_membership=TeamMembership,
    webhook=Webhook,
    webhook_event=WebhookEvent,
)


def spark_data_factory(model, json_data):
    """Factory function for creating SparkData objects.

    Args:
        model(basestring): The data model to use when creating the SparkData
            object (message, room, membership, etc.).
        json_data(basestring, dict): The JSON string or dictionary data with
            which to initialize the object.

    Returns:
        SparkData: The created SparkData object.

    Raises:
        TypeError: If the json_data parameter is not a JSON string or
            dictionary.

    """
    return spark_data_models[model](json_data)


def simple_data_factory(model, json_data):
    """Factory function for creating SimpleDataModel objects.

    Args:
        model(basestring): The data model to use when creating the SparkData
            object (message, room, membership, etc.).
        json_data(basestring, dict): The JSON string or dictionary data with
            which to initialize the object.

    Returns:
        SimpleDataModel: The created SimpleDataModel object.

    Raises:
        TypeError: If the json_data parameter is not a JSON string or
            dictionary.

    """
    return SimpleDataModel(json_data)


def dict_data_factory(model, json_data):
    """Factory function for creating SimpleDataModel objects.

    Args:
        model(basestring): The data model to use when creating the SparkData
            object (message, room, membership, etc.).
        json_data(basestring, dict): The JSON string or dictionary data with
            which to initialize the object.

    Returns:
        OrderedDict: An ordered dictionary with the contents of the Spark JSON
            object.

    Raises:
        TypeError: If the json_data parameter is not a JSON string or
            dictionary.

    """
    return json_dict(json_data)
