sinksh create account type kolab identifier kolabaccount name KolabAccount
sinksh create resource type sink.imap identifier kolabimap account kolabaccount server imaps://kolab:143 username john.doe@example.org password Welcome2KolabSystems
sinksh create resource type sink.mailtransport identifier kolabsmtp account kolabaccount server smtp://kolab:25 username john.doe@example.org password Welcome2KolabSystems
sinksh create resource type sink.davresource identifier kolabdav resourceUrl kolab/iRony/addressbooks/john.doe%40example.org  username john.doe@example.org  password Welcome2KolabSystems
sinksh create identity name "John Doe" address john.doe@example.org account kolabaccount

sinksh sync kolabimap
sinksh sync kolabdav
