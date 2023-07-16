#!/usr/bin/bash

sudo chmod +777 /dev/ttyACM0
sleep 5
gnome-terminal -- bash -c "roscore; bash"
sleep 5
gnome-terminal -- bash -c "rosserial_python serial_node.py /dev/ttyACM0; bash"
sleep 5
gnome-terminal -- bash -c "runserver.sh; bash"
sleep 1
gnome-terminal -- bash -c "websocket.sh"
sleep 1
exit 0