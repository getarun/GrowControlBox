temp=$(cat /sys/bus/w1/devices/28-000004ac246a/w1_slave | grep  -E -o ".{0,0}t=.{0,5}" | cut -c 3-)
echo "$temp"