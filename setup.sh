#! /bin/bash
echo "Excute setup.sh"

sudo apt update 
sudo apt upgrade
sudo apt install python3 -y
sudo apt install python3-pip -y
udo apt-get install git-core -y

./sublime.sh
./socket_io.sh
./sqlite3.sh
./ssh.sh
./remote-desktop-connection.sh
./pyqt.sh
./dht_11.sh
./flask.sh
./curl.sh
./ads1115.sh
