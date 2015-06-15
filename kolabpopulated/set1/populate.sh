#!/bin/bash
LDAPPW=test

for f in /data/*.ldif; do
    echo "Adding default user $f"
    ldapadd -x -h localhost -D "cn=Directory Manager" -w $LDAPPW -f $f || echo "error on create";
done

echo "Creating a bunch of shared mailboxes"
kolab create-mailbox shared/notype@example.org
kolab create-mailbox shared/notype/mail@example.org
kolab set-mailbox-metadata shared/notype/mail@example.org /shared/vendor/kolab/folder-type mail
kolab add-user-subscription john.doe@example.org "Shared Folders/shared/notype"
kolab add-user-subscription john.doe@example.org "Shared Folders/shared/notype/mail"

kolab create-mailbox user/jane.doe/Calendar/shared@example.org
kolab set-mailbox-metadata "user/jane.doe/Calendar/shared@example.org" /shared/vendor/kolab/folder-type event
kolab set-mailbox-acl "user/jane.doe/Calendar/shared@example.org" john.doe@example.org lrswipkxtecda
kolab create-mailbox user/jane.doe/Tasks/shared@example.org
kolab set-mailbox-metadata "user/jane.doe/Tasks/shared@example.org" /shared/vendor/kolab/folder-type task
kolab set-mailbox-acl "user/jane.doe/Tasks/shared@example.org" john.doe@example.org lrswipkxtecda
