sinksh create account type kolab identifier kolabnowAccount name KolabnowAccount
sinksh create resource type sink.imap identifier kolabnowImap account kolabnowAccount server imaps://imap.kolabnow.com:993 username test1@kolab.org password Welcome2KolabSystems
sinksh create resource type sink.mailtransport identifier kolabnowSmtp account kolabnowAccount server smtps://smtp.kolabnow.com:587 username test1@kolab.org password Welcome2KolabSystems
sinksh create resource type sink.davresource  identifier kolabnowDav account kolabnowAccount resourceUrl https://apps.kolabnow.com/addressbooks/test1%40kolab.org  username test1@kolab.org  password Welcome2KolabSystems

sinksh sync kolabnowImap
sinksh sync kolabnowDav
