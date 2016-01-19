unset DBUS_SESSION_BUS_PID

function setup {
    if [ -f ~/dbusenv ]
    then
	source ~/dbusenv
    else
	touch ~/dbusenv
    fi

    if [ -z "$DBUS_SESSION_BUS_PID" ]
    then
	dbus-launch --sh-syntax > ~/dbusenv
	echo "started dbus"
    else
	echo "dbus at $DBUS_SESSION_BUS_ADDRESS"
	echo "dbus at $DBUS_SESSION_BUS_PID"

	if ps -p $DBUS_SESSION_BUS_PID > /dev/null
	then
	    echo "dbus is running"
	else
	    echo "dbus killed, starting again"
	    dbus-launch --sh-syntax > ~/dbusenv
	    echo "started dbus"
	fi
    fi
    source ~/dbusenv
}
setup
