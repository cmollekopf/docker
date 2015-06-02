import json
from client import Client


def createResourceList(client):
    import os, random

    f = open(os.path.join(os.path.dirname(__file__), 'data/resourceslist.cvs')).read()
    resources = f.split('\n')

    client.resource_type_list()

    rList = []

    for resource in resources[10:15]:
        rList.append({"type_key": random.choice(c.resourceKeys.keys()), "cn": resource})

    return rList

def createResources(client, rList):
    client.resource_type_list()
    for r in rList:
        c.add_resource(**r)

if __name__ == "__main__":
    c = Client()

    try:
        f = open('/data/resources.list').read()
        rlist = json.loads(f)['rlist']
        createResources(c, rlist)
    except IOError:
        print "create rList"
        rlist = createResourceList(c)
        with open('/data/resources.list','w') as f:
            f.write(json.dumps({"rlist":rlist}))
        createResources(c, rlist)

