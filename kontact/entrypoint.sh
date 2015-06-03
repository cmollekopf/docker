source ~/kdeenv.sh
source ~/setupdbus.sh
# Use same graphics system as host, since we'll share the X11 socket
export QT_GRAPHICSSYSTEM=opengl
export QT_X11_NO_MITSHM=1
# Give access to graphics card. Alternatively add user to group video
sudo setfacl -m user:developer:rw /dev/dri/card0

kwalletd&
export IMAP_TRACE=1
akonadictl start &> /tmp/akonadi.output
dbus-monitor --session interface='org.freedesktop.Notifications',member='Notify' &> /tmp/notifications.output &

# Block until akonadi is started so we don't accidentaly start akonadi again
while ! qdbus org.freedesktop.Akonadi.Control / org.freedesktop.DBus.Peer.Ping; do sleep 1 && echo sleep; done; echo "done"
while ! qdbus org.freedesktop.Akonadi.Resource.akonadi_kolab_resource_0 / org.freedesktop.DBus.Peer.Ping; do sleep 1 && echo sleep; done; echo "done"

function syncCollection() {
    qdbus org.freedesktop.Akonadi.Resource.akonadi_kolab_resource_0 / org.freedesktop.Akonadi.Resource.synchronizeCollection $1
}
