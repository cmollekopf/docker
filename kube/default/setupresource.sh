sinksh create account type maildir identifier maildiraccount1 name MaildirAccount
sinksh create resource identifier maildirresource1 account maildiraccount1 type sink.maildir path /home/developer/maildir1
sinksh sync maildirresource1
