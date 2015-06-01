import os
import random

from pykolab import utils

from client import Client

# This means each iteration will do what it does at most this many plus
# one times. '5' means 5*5 + 5*5 entries.
max_multiplier = 5

# This means three in four entries is a contact, and not a kolab user
ratio_contacts = 0

def create_users(client):
    bfp = open(os.path.join(os.path.dirname(__file__), 'data/de-boys.txt'), 'r')
    gfp = open(os.path.join(os.path.dirname(__file__), 'data/de-girls.txt'), 'r')
    sfp = open(os.path.join(os.path.dirname(__file__), 'data/de-surnames.txt'), 'r')

    boys = [x.strip() for x in bfp.readlines()]
    girls = [x.strip() for x in gfp.readlines()]
    surnames = [x.strip() for x in sfp.readlines()]

    bfp.close()
    gfp.close()
    sfp.close()

    for g in range(0, (len(girls)-1)):
        if g >= max_multiplier and not max_multiplier < 0:
            break

        for s in range(0, (len(surnames)-1)):
            if s >= max_multiplier and not max_multiplier < 0:
                break

            # Contact or Kolab User?
            contact = random.randint(0,ratio_contacts)
            givenname = girls[random.randint(0,(len(girls)-1))]
            sn = surnames[random.randint(0,(len(surnames)-1))]

            if contact > 0:
                type_key = 'contact'
                attrs = {
                        'ou': "ou=Contacts,%s" % client.conf.get('ldap','user_base_dn'),
                        'mail': '%s.%s@example.org' % (
                                utils.translate(givenname, 'de_DE'),
                                utils.translate(sn, 'de_DE')
                            )
                    }

            else:
                type_key = 'kolab'
                ou_info = client.random_ou(params={'ou': 'People'})
                attrs = {
                        'ou': ou_info['entrydn']
                    }

            client.add_user(
                    givenname,
                    sn,
                    preferredlanguage='de_DE',
                    type_key = type_key,
                    attrs = attrs
                )

c = Client()

create_users(c)
