#! /bin/bash
echo "Excute dht_11.sh"

cd ~/Downloads
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo apt-get install build-essential python3-dev -y
sudo python3 setup.py install 
