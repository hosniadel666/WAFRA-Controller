#! /bin/bash
echo "Excute sublime.sh"

wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get install sublime-text

#################################
#	IN PASPBERRY PI SIDE	#
#################################
sudo apt-get install pure-ftpd -y

#################################    
#  IN PERSONAL COMPUTER  SIDE   #
#################################
# inside sublime : ctrl+shift+p
# then : write install
# then : write sftp
# then : specify ip of rpi and 
#	 remote path
# then : upload when save:trur
#################################
