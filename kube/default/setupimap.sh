sinksh create account type imap identifier imapaccount1 name ImapAccount
sinksh create resource type sink.imap identifier imapresource1 account imapaccount1 server imaps://kolab:143 username john.doe@example.org password Welcome2KolabSystems
sinksh create resource type sink.mailtransport identifier smtpresource1 account imapaccount1 server smtp://kolab:25 username john.doe@example.org password Welcome2KolabSystems
sinksh create identity name "John Doe" address doe@example.org account imapaccount1
sinksh sync imapresource1
