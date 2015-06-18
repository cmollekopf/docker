<?php
    $config['kolab_folders_configuration_default'] = 'Configuration';
    $config['kolab_folders_event_default'] = 'Calendar';
    $config['kolab_folders_contact_default'] = 'Contacts';
    $config['kolab_folders_task_default'] = 'Tasks';
    $config['kolab_folders_note_default'] = 'Notes';
    $config['kolab_folders_file_default'] = 'Files';
    $config['kolab_folders_freebusy_default'] = 'Freebusy';
    $config['kolab_folders_journal_default'] = 'Journal';
    $config['kolab_folders_mail_inbox'] = 'INBOX';
    $config['kolab_folders_mail_drafts'] = 'Drafts';
    $config['kolab_folders_mail_sentitems'] = 'Sent';
    $config['kolab_folders_mail_junkemail'] = 'Spam';
    $config['kolab_folders_mail_outbox'] = '';
    $config['kolab_folders_mail_wastebasket'] = 'Trash';

    if (file_exists(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__))) {
        include_once(RCUBE_CONFIG_DIR . '/' . $_SERVER["HTTP_HOST"] . '/' . basename(__FILE__));
    }

?>
