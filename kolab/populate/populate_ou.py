from client import Client

def ouStructure(client):

    base_dn = client.conf.get('ldap', 'base_dn')

    ous = []

    departments = [
            "IT",
            "Finance",
            "Human Resources",
            "Marketing",
            "Sales",
            "Services",
            "Research & Development",
            "Purchasing",
            "Legal",
            "Quality Assurance",
            "Management",
            "Engineering",
            "Supply Chain Management"
    ]

    for department in departments:
        ous.extend(
                [
                    {'ou': department, 'description': department, 'base_dn': "%s" % base_dn},
                    {'ou': 'People', 'description': department, 'base_dn': "ou=%s,%s" % (department, base_dn)},
                    {'ou': 'Resource', 'description': department, 'base_dn': "ou=%s,%s" % (department, base_dn)},
                    {'ou': 'Group', 'description': department, 'base_dn': "ou=%s,%s" % (department, base_dn)},
                ]
        )

    for ou in ous:
        client.ou_add(ou)


c = Client()

ouStructure(c)
