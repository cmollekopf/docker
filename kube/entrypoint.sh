export QML_IMPORT_PATH=/work/install/lib64/qml
export QML2_IMPORT_PATH=/work/install/lib64/qml
export QT_PLUGIN_PATH=/work/install/lib64/plugins/:$QT_PLUGIN_PATH
export LD_LIBRARY_PATH=/work/install/lib64
export PATH=/work/install/bin:$PATH

# Use same graphics system as host, since we'll share the X11 socket
export QT_GRAPHICSSYSTEM=native
export QT_X11_NO_MITSHM=1
# Give access to graphics card. Alternatively add user to group video
sudo setfacl -m user:developer:rw /dev/dri/card0
