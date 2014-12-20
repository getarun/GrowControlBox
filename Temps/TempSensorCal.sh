sensor1=$(cat /sys/bus/w1/devices/28-000004ac246a/w1_slave | grep  -E -o ".{0,0}t=.{0,5}" | cut -c 3-)
sensor2=$(cat /sys/bus/w1/devices/28-00042e08a9ff/w1_slave | grep  -E -o ".{0,0}t=.{0,5}" | cut -c 3-)
sensor3=$(cat /sys/bus/w1/devices/28-00042e07e7ff/w1_slave | grep  -E -o ".{0,0}t=.{0,5}" | cut -c 3-)
sensor4=$(cat /sys/bus/w1/devices/28-00042e08d5ff/w1_slave | grep  -E -o ".{0,0}t=.{0,5}" | cut -c 3-)
echo "Sensor 1: $sensor1"
echo "Sensor 2: $((sensor2 + 125))"
echo "Sensor 3: $((sensor3 - 63))"
echo "Sensor 4: $((sensor4 - 125))"