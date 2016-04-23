# -*- coding: utf-8 -*-

# request.requires_https()
import string
import random
import uuid
import datetime
import os

from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth, AuthJWT

myconf = AppConfig(reload=True)

VALID_APPLICATION_STATUSES = ["incomplete","pending","approved","declined", "deleted"]
VALID_LOAN_TYPES = ["personal","unsecured", "corprate", "secured"]
VALID_ATTACHMENT_TYPES = ["W2","Void Check", "Utility Bill"]


EXTRA_AUTH_FIELDS = [
                     Field('access_token','string')
                    ]
