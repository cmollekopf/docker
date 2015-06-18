<?php
    // This will overwrite defined LDAP filter
    // Note: LDAP addressbook defined for kolab_auth plugin is used
    $config['kolab_delegation_filter'] = '(|(objectClass=kolabInetOrgPerson)(&(objectclass=kolabsharedfolder)(kolabFolderType=mail)))';

    // Delegates field (from fieldmap configuration) to get delegates list
    // Note: This is a field name, not LDAP attribute name
    // Note: LDAP addressbook defined for kolab_auth plugin is used
    $config['kolab_delegation_delegate_field'] = 'kolabDelegate';

    // User authentication ID field (from fieldmap configuration)
    // See kolab_auth plugin config
    $config['kolab_delegation_login_field'] = 'email';

    // Use this fields (from fieldmap configuration) for identities
    // If the value array contains more than one field, first non-empty will be used
    // Note: These are not LDAP attributes, but field names in config
    // Note: If there are more than one email address, as many identities will be created
    // See kolab_auth plugin config
    $config['kolab_delegation_name_field']  = array('name', 'cn');
    $config['kolab_delegation_email_field'] = array('email');

    // Remove all user identities which do not match the users primary or alias
    // addresses and delegators addresses
    $config['kolab_delegation_purge_identities'] = false;
?>
