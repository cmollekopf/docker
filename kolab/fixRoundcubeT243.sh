#/bin/sh

# Script to wrok around https://git.kolab.org/T243
# Execute in /usr/share/roundcubemail
cd /usr/share/roundcubemail
curl -sS https://getcomposer.org/installer | php

(
    echo '{'
    echo '  "name": "kolab/roundcubemail",'
    echo '  "description": "Roundcube Webmail for Kolab",'
    echo '  "license": "GPL-3.0",'
    echo '  "require": { "php": ">=5.3.3" },'
    echo '  "autoload": {'
    echo '    "psr-0": { "": "/usr/share/pear/" },'
    echo '    "psr-4": { "": "/usr/share/php/" }'
    echo '  }'
    echo '}'
) > composer.json

php composer.phar update
