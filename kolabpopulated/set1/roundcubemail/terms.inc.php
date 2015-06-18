<?php

    /* terms plugin */

    // log accepted terms
    $config['terms_log'] = true;

    // renew agreement if older than YYYY-MM-DD HH:MM:SS
    // NOTICE: Must be in past and set accordingly to server Timezone!!!
    $config['terms_date'] = '2011-02-24 00:00:00';

    // renew agreement automatically afer x days
    $config['terms_renew'] = 28; // 0 = never

    // always request terms agreement after login
    $config['terms_always'] = false;

    if (file_exists(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__))) {
        include_once(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__));
    }

?>
