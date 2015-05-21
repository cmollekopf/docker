source ~/kdeenv.sh
source ~/setupdbus.sh
# Use same graphics system as host, since we'll share the X11 socket
export QT_GRAPHICSSYSTEM=opengl
export QT_X11_NO_MITSHM=1
# Give access to graphics card. Alternatively add user to group video
sudo setfacl -m user:developer:rw /dev/dri/card0

kwalletd&
akonadictl start &> /tmp/akonadi.output
