<?php

    // The id of the LDAP address book (which refers to the rcmail_config['ldap_public'])
    // or complete addressbook definition array.
    $config['kolab_auth_addressbook'] = Array(
        'name'                      => 'Kolab Auth',
        'hosts'                     => Array('localhost'),
        'port'                      => 389,
        'use_tls'                   => false,
        'user_specific'             => false,
        'base_dn'                   => 'dc=example,dc=org',
        'bind_dn'                   => 'uid=kolab-service,ou=Special Users,dc=example,dc=org',
        'bind_pass'                 => 'b92PQ9PyWzfraJb',
        'writable'                  => false,
        'ldap_version'              => 3,       // using LDAPv3
        'fieldmap'                  => Array(
                'name'              => 'displayname',
                'email'             => 'mail',
                'email:alias'       => 'alias',
                'role'              => 'nsroledn',
            ),
        'sort'                      => 'displayname',
        'scope'                     => 'sub',
        'filter'                    => '(objectClass=*)',
        'fuzzy_search'              => true,
        'sizelimit'                 => '0',
        'timelimit'                 => '0',
        'groups'                    => Array(
                'base_dn'           => 'ou=Groups,dc=example,dc=org',
                'filter'            => '(|(objectclass=groupofuniquenames)(objectclass=groupofurls))',
                'object_classes'    => Array('top', 'groupOfUniqueNames'),
                'member_attr'       => 'uniqueMember',
            ),
    );


    // This will overwrite defined filter
    $config['kolab_auth_filter'] = '(&' . '(objectclass=inetorgperson)' . '(|(uid=%u)(mail=%fu)(alias=%fu)))';

    // Use this fields (from fieldmap configuration) to get authentication ID
    $config['kolab_auth_login'] = 'email';

    // Use this fields (from fieldmap configuration) for default identity
    $config['kolab_auth_name']  = 'name';
    $config['kolab_auth_alias'] = 'alias';
    $config['kolab_auth_email'] = 'email';

    if (preg_match('/\/helpdesk-login\//', $_SERVER["REQUEST_URI"]) ) {

        // Login and password of the admin user. Enables "Login As" feature.
        $config['kolab_auth_admin_login']    = 'cyrus-admin';
        $config['kolab_auth_admin_password'] = 'XeAvGufVOGJtOX3';

        $config['kolab_auth_auditlog'] = true;
    }

    // Administrative role field (from fieldmap configuration) which must be filled with
    // specified value which adds privilege to login as another user.
    $config['kolab_auth_role']       = 'role';
    $config['kolab_auth_role_value'] = 'cn=kolab-admin,dc=example,dc=org';

    // Administrative group name to which user must be assigned to
    // which adds privilege to login as another user.
    $config['kolab_auth_group'] = 'Kolab Helpdesk';

    if (file_exists(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__))) {
        include_once(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__));
    }

?>
