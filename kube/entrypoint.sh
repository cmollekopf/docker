export QML_IMPORT_PATH=/work/install/lib64/qml
export QML2_IMPORT_PATH=/work/install/lib64/qml
export QT_PLUGIN_PATH=/work/install/lib64/plugins/:$QT_PLUGIN_PATH
export LD_LIBRARY_PATH=/work/install/lib64
export PATH=/work/install/bin:$PATH

export XDG_CONFIG_DIRS=/work/install/share/config:$XDG_CONFIG_DIRS
export XDG_DATA_DIRS=/work/install/share/:/usr/share:$XDG_DATA_DIRS

# Use same graphics system as host, since we'll share the X11 socket
export QT_GRAPHICSSYSTEM=native
export QT_X11_NO_MITSHM=1
# Give access to graphics card. Alternatively add user to group video
sudo setfacl -m user:developer:rw /dev/dri/card0

export KDE_FULL_SESSION=true
export KDE_SESSION_UID=`id -ru`
export KDE_SESSION_VERSION=5
export XDG_CURRENT_DESKTOP=KDE
# A QPA plugin that allows us to configure stuff
export QT_QPA_PLATFORMTHEME=qt5ct
# The qt5ct configuration already does this for us
#export QT_STYLE_OVERRIDE=breeze
# Breeze doesn't look very good somehow
export QT_QUICK_CONTROLS_STYLE=Desktop
