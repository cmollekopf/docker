function printKDEenv {
    echo "KDEHOME: $KDEHOME"
    echo "KDEDIR: $KDEDIR"
    echo "KDEDIRS: $KDEDIRS"
    echo "BUILD_DIR: $BUILD_DIR"
    echo "PATH: $PATH"
    echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
    echo "PKG_CONFIG_PATH: $PKG_CONFIG_PATH"
    echo "QT_PLUGIN_PATH: $QT_PLUGIN_PATH"
}

function akonadidb {
    mysql --auto-vertical-output -S $XDG_DATA_HOME/akonadi/socket-*/mysql.socket akonadi
}

export KDE_FULL_SESSION=true
export KDE_SESSION_UID=`id -ru`
export KDE_SESSION_VERSION=4
export XDG_CURRENT_DESKTOP=KDE

