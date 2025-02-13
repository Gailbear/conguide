#!/usr/bin/env python

# Copyright (c) 2015-2017, Paul Selkirk
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.


from functools import reduce
import json
from datetime import datetime, timezone

from . import config
from .participant import Participant
from .session import Session

sessions = []
participants = {}

def read(fn):
    """ Read an XML file, return a list of sessions and a dict of participants. """

    global sessions, participants

    if sessions:
        return (sessions, participants)

    program = []
    people = []
    with open(fn, 'r') as f:
        program = json.loads(f.readline()[12:])
        people = json.loads(f.readline()[11:])

    # people_by_id = dict(map(lambda p: (p['id'], p), people))

    # print(program[0])

    def transform_program_item(p):
        participants = map(lambda p: p['name'], p['people'])
        try:
            moderators = map(lambda p: p['name'], filter(lambda p: p.get('role', '') == "moderator", p['people']))
        except KeyError:
            moderators = []
        date =  datetime.fromisoformat(p['datetime'][:-5])

        date = date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        new_p = {
            'sessionid': p['id'],
            'room': p['loc'][0],
            'title': p['title'],
            'description': p['desc'],
            'participants': participants,
            'moderators': moderators,
            'day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][date.weekday()],
            'time': date.strftime("%H:%M"),
            'duration': "{}".format(p['mins']),
            'tracks': [x['label'] for x in p['tags'] if x['category'] == 'Area'],
            'type': p['format'],
            'tags': []
        }
        return new_p

    sessions = map(lambda p: Session(transform_program_item(p), participants), program)
    sessions = sorted(sessions)
    for i in range(len(sessions)):
        sessions[i].index = i + 1

    # add participant metadata
    people_by_name = reduce(lambda prev, part: {**prev, part['name']: part}, people, {})
    for p in participants.items():
        person = people_by_name[p[0]]
        if person['bio']:
            p[1].bio = person['bio']
        p[1].links = person['links']
        #p[1].id = person['id']
    return (sessions, participants)

def read_bios(fn, participants):
    return participants

    #for timeslot in xml.etree.ElementTree.parse(fn).getroot():
#     parser = xml.etree.ElementTree.XMLParser(encoding='utf-8')
#     for timeslot in xml.etree.ElementTree.parse(fn, parser).getroot():
#         assert timeslot.tag == 'time'
#         start = timeslot[0]
#         assert(start.tag == 'start')
#         day = start.findtext('day')
#         time = start.findtext('time')

#         for item in timeslot[1:]:
#             assert item.tag == 'item'
#             room = item.findtext('room')
#             venue = item.findtext('venue')
#             row = {'day':day, 'time':time, 'room':room, 'level':venue,
#                    'tracks':[], 'tags':[],
#                    'participants':[], 'moderators':[]}
#             for a in item:
#                 if a.tag == 'details':
#                     for b in a:
#                         if b.tag == 'tracks':
#                             for c in b:
#                                 row['tracks'].append(c.text)
#                         elif b.tag == 'tags':
#                             for c in b:
#                                 row['tags'].append(c.text)
#                         elif b.tag == 'people':
#                             for c in b:
#                                 name = c.findtext('name')
#                                 if name in participant.Participant.chname:
#                                     name = participant.Participant.chname[name]
#                                 row['participants'].append(name)
#                                 if c.tag == 'moderator':
#                                     row['moderators'].append(name)
#                         else:
#                             row[b.tag] = b.text
#                 else:
#                     row[a.tag] = a.text

#             row['sessionid'] = row['reference_number']
#             row['index'] = row['reference_number']
#             try:
#                 row['type'] = row['format']
#             except KeyError:
#                 row['type'] = ''

#             # error checking
#             if not row['reference_number']:
#                 if not config.quiet:
#                     print('warning: %s %s %s: empty reference_number element' %
#                           (row['day'], row['time'], row['title']))
#             tags = []
#             for t in row['tags']:
#                 if t in tags:
#                     if not config.quiet:
#                         print('warning: %s %s: duplicate tag %s' % \
#                               (row['reference_number'], row['title'], t))
#                 else:
#                     tags.append(t)
#             row['tags'] = tags

#             # cleanup
#             for k in row.keys():
#                 minimal = (k not in ['title', 'description'])
#                 row[k] = cleanup(row[k], minimal)

#             # make a new session from this data
#             s = session.Session(row, participants)
#             # if session is in [session do not print], the instance doesn't get
#             # initialized, and we can drop it (should we explicitly delete it?)
#             if hasattr(s, 'sessionid'):
#                 sessions.append(s)

#     # sort
    # sessions = sorted(sessions)

    # return (sessions, participants)

# def cleanup(field, minimal=False):
#     if type(field) is list:
#         for i, f in enumerate(field):
#             field[i] = cleanup(f)

#     elif (type(field) is str) or (not config.PY3 and type(field) is unicode):
#         # convert all whitespace (including newlines) to single spaces
#         if not config.PY3:
#             # python 2.7 doesn't recognize non-breaking space as whitespace
#             field = field.replace(u'\u00a0', ' ')
#         field = re.sub(r'\s+', ' ', field)

#         if not minimal:
#             # change bold to italic
#             field = re.sub(r'<(/?)em>', r'<\1i>', field)
#             field = re.sub(r'<(/?)strong>', r'<\1i>', field)

#             # change explicit line breaks to newline
#             field = re.sub(r'<br ?/> ?', r'\n', field)
#             field = re.sub(r'</p> ?<p> ?', r'\n', field)
#             field = re.sub(r'^<p>(.*)</p>$', r'\1', field)
#             field = re.sub(r' ?<p>', r'\n', field)
#             field = re.sub(r'</p>', r'', field)

#             # lists - hack for one session
#             field = re.sub(r' ?<ul> ?', r'', field)
#             field = re.sub(r' ?</ul> ?', r'\n\n', field)
#             field = re.sub(r'<li> ?', r'\n<li>', field)

#             # remove html tags we can't/won't support in print
#             field = re.sub(r'</?span.*?> ?', r'', field)
#             field = re.sub(r'</?div.*?> ?', r'', field)
#             field = re.sub(r'</?hr.*?> ?', r'', field)
#             field = re.sub(r'</?a.*?> ?', r'', field)
#             field = re.sub(r'</?font.*?> ?', r'', field)

#             # remove wtf
#             field = re.sub(u'\u00e2', '', field)

#         # remove extraneous whitespace
#         field = re.sub(r'^\s+', '', field) # leading space
#         field = re.sub(r'\s+$', '', field) # trailing space
#         field = re.sub(r'\s+([,.;])', r'\1', field) # space before punctuation

#     return field
