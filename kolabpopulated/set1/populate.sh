#!/bin/bash
LDAPPW=test

for f in /data/*.ldif; do
    echo "Adding default user $f"
    ldapadd -x -h localhost -D "cn=Directory Manager" -w $LDAPPW -f $f;
done

echo "Creating a bunch of shared mailboxes"
kolab create-mailbox shared/notype@example.org
kolab create-mailbox shared/notype/mail@example.org
kolab set-mailbox-metadata shared/notype/mail@example.org /shared/vendor/kolab/folder-type mail
kolab add-user-subscription john.doe@example.org "Shared Folders/shared/notype"
kolab add-user-subscription john.doe@example.org "Shared Folders/shared/notype/mail"
