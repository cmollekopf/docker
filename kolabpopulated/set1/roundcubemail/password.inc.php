<?php

    // Password Plugin options
    // -----------------------
    // A driver to use for password change. Default: "sql".
    // See README file for list of supported driver names.
    $config['password_driver'] = 'ldap_simple';

    // Determine whether current password is required to change password.
    // Default: false.
    $config['password_confirm_current'] = true;

    // Require the new password to be a certain length.
    // set to blank to allow passwords of any length
    $config['password_minimum_length'] = 6;

    // Require the new password to contain a letter and punctuation character
    // Change to false to remove this check.
    $config['password_require_nonalpha'] = false;

    // Enables logging of password changes into logs/password
    $config['password_log'] = true;


    // LDAP and LDAP_SIMPLE Driver options
    // -----------------------------------
    // LDAP server name to connect to.
    // You can provide one or several hosts in an array in which case the hosts are tried from left to right.
    // Exemple: array('ldap1.exemple.com', 'ldap2.exemple.com');
    // Default: 'localhost'
    $config['password_ldap_host'] = 'localhost';

    // LDAP server port to connect to
    // Default: '389'
    $config['password_ldap_port'] = '389';

    // TLS is started after connecting
    // Using TLS for password modification is recommended.
    // Default: false
    $config['password_ldap_starttls'] = false;

    // LDAP version
    // Default: '3'
    $config['password_ldap_version'] = '3';

    // LDAP base name (root directory)
    // Exemple: 'dc=exemple,dc=com'
    $config['password_ldap_basedn'] = 'ou=People,dc=example,dc=org';

    // LDAP connection method
    // There is two connection method for changing a user's LDAP password.
    // 'user': use user credential (recommended, require password_confirm_current=true)
    // 'admin': use admin credential (this mode require password_ldap_adminDN and password_ldap_adminPW)
    // Default: 'user'
    $config['password_ldap_method'] = 'user';

    // LDAP Admin DN
    // Used only in admin connection mode
    // Default: null
    $config['password_ldap_adminDN'] = null;

    // LDAP Admin Password
    // Used only in admin connection mode
    // Default: null
    $config['password_ldap_adminPW'] = null;

    // LDAP user DN mask
    // The user's DN is mandatory and as we only have his login,
    // we need to re-create his DN using a mask
    // '%login' will be replaced by the current roundcube user's login
    // '%name' will be replaced by the current roundcube user's name part
    // '%domain' will be replaced by the current roundcube user's domain part
    // '%dc' will be replaced by domain name hierarchal string e.g. "dc=test,dc=domain,dc=com"
    // Exemple: 'uid=%login,ou=people,dc=exemple,dc=com'
    // $config['password_ldap_userDN_mask'] = 'uid=%login,ou=people,dc=exemple,dc=com';

    // LDAP search DN
    // The DN roundcube should bind with to find out user's DN
    // based on his login. Note that you should comment out the default
    // password_ldap_userDN_mask setting for this to take effect.
    // Use this if you cannot specify a general template for user DN with
    // password_ldap_userDN_mask. You need to perform a search based on
    // users login to find his DN instead. A common reason might be that
    // your users are placed under different ou's like engineering or
    // sales which cannot be derived from their login only.
    $config['password_ldap_searchDN'] = 'uid=kolab-service,ou=Special Users,dc=example,dc=org';

    // LDAP search password
    // If password_ldap_searchDN is set, the password to use for
    // binding to search for user's DN. Note that you should comment out the default
    // password_ldap_userDN_mask setting for this to take effect.
    // Warning: Be sure to set approperiate permissions on this file so this password
    // is only accesible to roundcube and don't forget to restrict roundcube's access to
    // your directory as much as possible using ACLs. Should this password be compromised
    // you want to minimize the damage.
    $config['password_ldap_searchPW'] = 'b92PQ9PyWzfraJb';

    // LDAP search base
    // If password_ldap_searchDN is set, the base to search in using the filter below.
    // Note that you should comment out the default password_ldap_userDN_mask setting
    // for this to take effect.
    $config['password_ldap_search_base'] = 'ou=People,dc=example,dc=org';

    // LDAP search filter
    // If password_ldap_searchDN is set, the filter to use when
    // searching for user's DN. Note that you should comment out the default
    // password_ldap_userDN_mask setting for this to take effect.
    // '%login' will be replaced by the current roundcube user's login
    // '%name' will be replaced by the current roundcube user's name part
    // '%domain' will be replaced by the current roundcube user's domain part
    // '%dc' will be replaced by domain name hierarchal string e.g. "dc=test,dc=domain,dc=com"
    // Example: '(uid=%login)'
    // Example: '(&(objectClass=posixAccount)(uid=%login))'
    $config['password_ldap_search_filter'] = '(&(|(uid=%login)(mail=%login)(mailAlternateAddress=%login)(alias=%login))(objectclass=kolabinetorgperson))';

    // LDAP password hash type
    // Standard LDAP encryption type which must be one of: crypt,
    // ext_des, md5crypt, blowfish, md5, sha, smd5, ssha, or clear.
    // Please note that most encodage types require external libraries
    // to be included in your PHP installation, see function hashPassword in drivers/ldap.php for more info.
    // Default: 'crypt'
    $config['password_ldap_encodage'] = 'clear';

    // LDAP password attribute
    // Name of the ldap's attribute used for storing user password
    // Default: 'userPassword'
    $config['password_ldap_pwattr'] = 'userPassword';

    // LDAP password force replace
    // Force LDAP replace in cases where ACL allows only replace not read
    // See http://pear.php.net/package/Net_LDAP2/docs/latest/Net_LDAP2/Net_LDAP2_Entry.html#methodreplace
    // Default: true
    $config['password_ldap_force_replace'] = true;

    // LDAP Password Last Change Date
    // Some places use an attribute to store the date of the last password change
    // The date is meassured in "days since epoch" (an integer value)
    // Whenever the password is changed, the attribute will be updated if set (e.g. shadowLastChange)
    $config['password_ldap_lchattr'] = '';

    // LDAP Samba password attribute, e.g. sambaNTPassword
    // Name of the LDAP's Samba attribute used for storing user password
    $config['password_ldap_samba_pwattr'] = '';

    // LDAP Samba Password Last Change Date attribute, e.g. sambaPwdLastSet
    // Some places use an attribute to store the date of the last password change
    // The date is meassured in "seconds since epoch" (an integer value)
    // Whenever the password is changed, the attribute will be updated if set
    $config['password_ldap_samba_lchattr'] = '';

    if (file_exists(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__))) {
        include_once(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__));
    }

?>
