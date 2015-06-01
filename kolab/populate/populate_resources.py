import random
from client import Client

f = open('data/resourceslist.cvs').read()

resources = f.split('\n')

c = Client()
c.resource_type_list()

for resource in resources[10:15]:
    c.add_resource(random.choice(c.resourceKeys.keys()),resource)
