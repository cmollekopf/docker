<?php
    // ownCloud URL
    $config['owncloud_url'] = 'http://' . $_SERVER["HTTP_HOST"] . '/owncloud';

    if (file_exists(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__))) {
        include_once(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__));
    }

?>
