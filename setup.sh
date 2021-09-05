#! /bin/bash
echo "Excute setup.sh"

sudo apt update 
sudo apt upgrade
sudo apt install python3 -y
sudo apt install python3-pip -y
udo apt-get install git-core -y

./bash-scripts/sublime.sh
./bash-scripts/socket_io.sh
./bash-scripts/sqlite3.sh
./bash-scripts/ssh.sh
./bash-scripts/remote-desktop-connection.sh
./bash-scripts/pyqt.sh
./bash-scripts/dht_11.sh
./bash-scripts/flask.sh
./bash-scripts/curl.sh
./bash-scripts/ads1115.sh
