import pykolab

def login(wap_client):
    wap_client.API_HOSTNAME = "localhost"
    wap_client.API_BASE = "/kolab-webadmin/api/"
    wap_client.API_SCHEME = "http"
    wap_client.API_PORT="80"
    wap_client.API_SSL = False

    wap_client.authenticate("cn=Directory Manager", "test")


class Client:
    def wap(func):
        def wrapped(self, *args, **kwargs):
            from pykolab import wap_client
            self.wap_client = wap_client
            login(wap_client)
            return func(self, *args, **kwargs)
        return wrapped

    def __init__(self):
        self.primaryDomain = "example.org"
        self.resourceOu = u'ou=Resources,dc=example,dc=org'
        self.conf = pykolab.getConf()
        self.conf.finalize_conf()

    @wap
    def add_resource(self, type_key, cn, members=None, owner=None, **kw):

        if type_key == None or type_key == '':
            raise Exception

        if cn == None or cn == '':
            raise Exception

        resource_details = {
                'cn': cn,
                'kolabtargetfolder': "shared/Resources/%s@%s" % (
                        cn,
                        self.primaryDomain
                    ),
                'ou': self.resourceOu,
                'uniquemember': members,
                'owner': owner
            }

        resource_details.update(kw)

        type_id = self.resourceKeys[type_key]

        resource_type_info = self.resourceTypes['list'][type_id]['attributes']

        params = {}

        for attribute in resource_type_info['form_fields'].keys():
            attr_details = resource_type_info['form_fields'][attribute]

            if isinstance(attr_details, dict):
                if not attr_details.has_key('optional') or attr_details['optional'] == False or resource_details.has_key(attribute):
                    print params, attribute, resource_details
                    params[attribute] = resource_details[attribute]
            elif isinstance(attr_details, list):
                params[attribute] = resource_details[attribute]

        fvg_params = params
        fvg_params['object_type'] = 'resource'
        fvg_params['type_id'] = type_id
        fvg_params['attributes'] = [attr for attr in resource_type_info['auto_form_fields'].keys() if not attr in params.keys()]

        result = self.wap_client.resource_add(fvg_params)

        if not result:
            result = self.wap_client.resource_find({'cn': fvg_params['cn']})

        result = self.wap_client.resource_info(result['id'])

        return result

    @wap
    def resource_type_list(self):
        self.resourceTypes = self.wap_client.resource_types_list()
        self.resourceKeys = {i['key']:k for k,i in self.resourceTypes['list'].items() if k != '1'}

    @wap
    def add_user(self, givenname, sn, preferredlanguage='de_DE', type_key='kolab', attrs={}):

        if givenname == None:
            raise Exception

        if givenname == '':
            raise Exception

        if sn == None:
            raise Exception

        if sn == '':
            raise Exception

        user_details = attrs

        user_details['givenname'] = givenname
        user_details['sn'] = sn

        if not attrs.has_key('userpassword'):
            user_details['userpassword'] = '123456'

        if not attrs.has_key('ou'):
            user_details['ou'] = self.conf.get('ldap', 'user_base_dn')

        if not attrs.has_key('preferredlanguage'):
            user_details['preferredlanguage'] = preferredlanguage

        user_types = self.wap_client.user_types_list()

        user_type_id = 0

        for key in user_types['list'].keys():
            if user_types['list'][key]['key'] == type_key:
                user_type_id = key

        user_type_info = user_types['list'][user_type_id]['attributes']

        params = {
                'type_id': user_type_id,
                'user_type_id': user_type_id,
            }

        for attribute in user_type_info['form_fields'].keys():
            attr_details = user_type_info['form_fields'][attribute]

            if isinstance(attr_details, dict):
                if not attr_details.has_key('optional') or attr_details['optional'] == False:
                    params[attribute] = user_details[attribute]
            elif isinstance(attr_details, list):
                params[attribute] = user_details[attribute]

        for attribute in user_details.keys():
            if not params.has_key(attribute):
                params[attribute] = user_details[attribute]

        fvg_params = params
        fvg_params['object_type'] = 'user'
        fvg_params['type_id'] = user_type_id
        fvg_params['attributes'] = [attr for attr in user_type_info['auto_form_fields'].keys() if not attr in params.keys()]

        exec("retval = self.wap_client.form_value_generate(%r)" % (fvg_params))

        for attribute in user_type_info['auto_form_fields'].keys():
            if retval.has_key(attribute):
                fvg_params[attribute] = retval[attribute]

        result = self.wap_client.user_add(fvg_params)

        return result

    @wap
    def random_ou(self, params={}):
        import math
        import random

        ou = None

        search = {
                'search': {
                    'params': {
                        'objectclass': {
                            'value': 'organizationalunit',
                            'type': 'exact'
                            }
                        },
                    'operator': 'AND'
                    }
                }

        for (k,v) in params.iteritems():
            search['search']['params'][k] = { 'value': v, 'type': 'exact' }

        #print "search:", search

        ous = self.wap_client.ous_list(search)

        #print "ous:", '\n'.join(ous['list'].keys())

        num_ous = ous['count']

        #print "num_ous:", num_ous

        page_ous = len(ous['list'])

        #print "page_ous:", page_ous

        num_pages = (int)(math.floor(float(num_ous) / float(page_ous)))

        #print "num_pages:", num_pages

        # Continue stabbing at it.
        while True:
            try:
                page = random.randint(1, num_pages)
                ous = self.wap_client.ous_list(search)
                #print "ous:", '\n'.join(ous['list'].keys())
                ou = ous['list'].keys()[random.randint(0, (len(ous['list'])-1))]
                #print "ou:", ou
            except:
                pass
            finally:
                break

        ou_info = self.wap_client.ou_info(ou)
        #print "ou_info:", ou_info
        return ou_info


