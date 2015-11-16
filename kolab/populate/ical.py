#!/usr/bin/python
# -*- coding: utf-8 -*- 

""" Copyright Sandro Knauß <knauss@kolabsys.com>
    v0.1

    License: GPL 2+

    needs following python modules in brackets the version I used:
    icalendar (3.8.3)
    pytz (2014.7)

    for the ldap part:
    python-ldap (2.4.16)
"""
from icalendar import Calendar, Event
from icalendar import vCalAddress, vText
import random
import uuid
import pytz
from datetime import datetime, timedelta

class Address:
    """A class for attendees or resource lines in vevent"""
    def __init__(self, name, mail):
        self.name = name
        self.mail = mail

    def toVCalAdddress(self):
        """A attendee line in vevent"""
        address = vCalAddress('MAILTO:%s'%self.mail)
        address.params['cn'] = vText(self.name)
        return address

me = Address("Jens Eisenberg","jens.eisenberg@lhm.klab.cc")

attendees = [
            Address("John Doe", "john.doe@example.com"),
            Address("Alec Hubner", "alec.hubner@example.com")
            ]

resources = [
            Address("Meeting room 1","meetingroom1@example.com"),
            Address("Beamer 1","beamer1@example.com"),
            ]

LOCATIONS = ["Berlin", "Moskau", "Kolab office", "Meeting room", "Heaven", "Hell", "Tree"]
SUMMARIES = ["Vacation", "Wedding", "Kickoff", "Sprint meeting", "Eating", "Drinking"]

PARTSTAT = ["NEEDS-ACTION", "ACCEPTED", "DECLINED", "TENTATIVE"]
RSVP = ["TRUE", "FALSE"]
ROLE = ["REQ-PARTICIPANT"]

#in hours
DURATIONS=[1,2,4,6,8]

def createAttendee(address):
    """create a complete random attendee entry for a event for the address"""
    attendee = address.toVCalAdddress()
    attendee.params['CUTYPE'] = vText('INDIVIDUAL')
    attendee.params['PARTSTAT'] = vText(random.choice(PARTSTAT))
    attendee.params['RSVP'] = vText(random.choice(RSVP))
    attendee.params['ROLE'] = vText(random.choice(ROLE))
    return attendee

def createResource(address):
    """create a complete random resource entry for a event for the address"""
    resource = createAttendee(address)
    resource.params['CUTYPE'] = vText('RESOURCE')
    return resource

def createEvent(start, end):
    """create an VEVENT entry
    with start and end for the start and endtime"""
    event = Event()

    event['uid'] = uuid.uuid1()
    event.add('dtstart', start)
    event.add('dtend', end)
    dtstamp = datetime.now(pytz.UTC) - timedelta(seconds=random.randint(0,999999))
    if start < dtstamp:
        dtstamp = start - timedelta(seconds=random.randint(0,999999))
    event.add('dtstamp', dtstamp)
    del event['dtstart'].params['VALUE']
    del event['dtend'].params['VALUE']
    del event['dtstamp'].params['VALUE']
    event['location'] = random.choice(LOCATIONS)
    event['summary'] = random.choice(SUMMARIES)

    #me as organizer
    if random.randint(0,1):
        event['organizer'] = me.toVCalAdddress()
        #me as attendee
        if random.randint(0,1):
            event.add('attendee', createAttendee(me))
    else:
        event['organizer'] = random.choice(attendees).toVCalAdddress()
        #me should be attendee otherwise he is not part of the event at all
        event.add('attendee', createAttendee(me))

    random.shuffle(attendees)
    random.shuffle(resources)
    #at least on attendee
    for a in attendees[1:random.randint(1,10)]:
        event.add('attendee', createAttendee(a))
    for r in resources[0:random.randint(0,10)]:
        event.add('attendee', createResource(r))

    return event

def createCalendar(start, end, anz):
    """creates a calender with anz events, that are between start and end"""
    cal = Calendar()

    cal.add('prodid', '-//populate.py//knauss@kolabsys.com//')
    cal.add('version', '2.0')

    duration = (end-start).total_seconds()//3600
    for i in range(anz):
        s = start + timedelta(hours=random.randint(0,duration))
        cal.add_component(createEvent(s,s+timedelta(hours=random.choice(DURATIONS))))

    return cal


def saveCalender(cal,fname):
    """save the calender to a file"""
    with open(fname, 'wb') as f:
        f.write(cal.to_ical())

def ldapToFiles(host,username, password, base):
    """use ldap to create a attendee and resource list"""
    import ldap
    l = ldap.initialize("ldap://ldap.lhm.klab.cc:389")
    l.bind_s(username, password)
    ps = l.search_s(base,ldap.SCOPE_SUBTREE,'(&(objectClass=person)(mail=*))',['cn','mail'])
    with open("attendees.cvs", "w") as f:
        f.write("\n".join(["%s\t%s\t%s"%(i[0], i[1]["mail"][0], i[1]["cn"][0]) for i in ps]))
    ps = l.search_s(base,ldap.SCOPE_SUBTREE,'(&(kolabFolderType=event)(mail=*))',['cn','mail'])
    with open("resources.cvs", "w") as f:
        f.write("\n".join(["%s\t%s\t%s"%(i[0], i[1]["mail"][0], i[1]["cn"][0]) for i in ps]))

def read():
    """read the files into attendee and resource lists"""
    global attendees, resources, LOCATIONS
    with open("attendees.cvs") as f:
        lines = f.readlines()
        if len(lines) > 0:
            attendees=[]
            for l in lines:
                uid, mail, cn = l.split("\t")
                if mail.strip() == me.mail:
                    continue
                attendees.append(Address(cn.strip(),mail.strip()))

    with open("resources.cvs") as f:
        lines = f.readlines()
        if len(lines) > 0:
            resources=[]
            for l in lines:
                uid, mail, cn = l.split("\t")
                resources.append(Address(cn.strip(),mail.strip()))


    with open("cities.cvs") as f:
        lines = f.readlines()
        if len(lines) > 0:
            LOCATIONS = [i.strip() for i in lines]

#ok lets create a calendar

if __name__ == '__main__':
    anz = 10000
    read()
    cal = createCalendar(datetime(2005,1,1,0,0,0,tzinfo = pytz.timezone("Europe/Berlin")),
                         datetime(2015,12,31,23,59,59,tzinfo = pytz.timezone("Europe/Berlin")),
                         anz)
    name = me.name.lower().replace(" ",".")
    saveCalender(cal, "/tmp/%s%s.ics"%(name,anz))
