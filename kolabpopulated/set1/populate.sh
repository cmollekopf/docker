#!/bin/bash
LDAPPW=test
LDIFFILE=/data/doe.ldif
LDIFFILE2=/data/jane.ldif

echo "Adding default user: doe@example.org Welcome2KolabSystems"
ldapadd -x -h localhost -D "cn=Directory Manager" -w $LDAPPW -f $LDIFFILE
echo "Adding a second user: doe2@example.org (it's Jane!) Welcome2KolabSystems"
ldapadd -x -h localhost -D "cn=Directory Manager" -w $LDAPPW -f $LDIFFILE2

echo "Creating a bunch of shared mailboxes"
kolab create-mailbox shared/notype@example.org
kolab create-mailbox shared/notype/mail@example.org
kolab set-mailbox-metadata shared/notype/mail@example.org /shared/vendor/kolab/folder-type mail
kolab add-user-subscription john.doe@example.org "Shared Folders/shared/notype"
kolab add-user-subscription john.doe@example.org "Shared Folders/shared/notype/mail"
