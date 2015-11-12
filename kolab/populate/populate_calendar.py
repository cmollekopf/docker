#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Copyright Sandro Knauß <knauss@kolabsys.com>
    v0.1

    License: GPL 2+

    Add events to user calendar on a kolab server.
"""
import pytz
from datetime import datetime

import ical

import pykolab
from pykolab import imap_utf7
from pykolab.imap import IMAP
from pykolab.xml import event_from_ical

def calendar(user):
    return imap_utf7.encode( "user/{username}/Calendar@example.org".format(username=user))

def appendEvent(user, event):
    """event must be a ical object (python icalendar Event)"""
    e = event_from_ical(event) # construct a kolab object
    folder = calendar(user)
    imap.append(folder, None, None, e.to_message().as_string())

if __name__ == '__main__':
    conf = pykolab.getConf()
    conf.finalize_conf()

    imap = IMAP()
    imap.connect()

    user = "john.doe"

    start = datetime(2015, 1, 1, 0, 0, 0, tzinfo=pytz.timezone("Europe/Berlin"))
    end = datetime(2015, 1, 1, 10, 0, 0, tzinfo=pytz.timezone("Europe/Berlin"))
    event = ical.createEvent(start, end)

    # Admin normally has no right to do anything with the mailbox
    # so first add the right to append message (i) after adding the message
    # remove the right again
    imap.set_acl(calendar(user), 'cyrus-admin', 'lrsi')
    try:
        appendEvent(user, event)
    finally:
        imap.set_acl(calendar(user), 'cyrus-admin', '')
