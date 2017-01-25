sinksh create resource type sink.davresource  identifier dav1 resourceUrl https://apps.kolabnow.com/addressbooks/test1%40kolab.org  username test1@kolab.org  password Welcome2KolabSystems
sinksh sync dav1
sinksh list folder dav1 --show-all
