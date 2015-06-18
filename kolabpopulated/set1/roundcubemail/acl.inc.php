<?php
    $config['acl_advanced_mode'] = false;
    $config['acl_users_source'] = 'kolab_addressbook';
    $config['acl_users_field'] = 'mail';
    $config['acl_users_filter'] = 'objectClass=kolabInetOrgPerson';

    $config['acl_groups'] = true;
    $config['acl_group_prefix'] = 'group:';

    if (file_exists(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__))) {
        include_once(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__));
    }

?>
