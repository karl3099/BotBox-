sudo apt update

sudo apt upgrade

cd /lib/udev

sudo cp /home/greenbean/Desktop/60-ftdi232RL.rules 60-ftdi232RL.rules

cd rules.d

sudo ln ../60-ftdi232RL.rules 60-ftdi232RL.rules

sudo /etc/init.d/udev restart

sudo apt install gtkterm

sudo apt install python3.6

sudo apt install python3 idle

sudo apt install python3-pip

sudo -H pip3 install pyserial==3.4

sudo -H pip3 install pandas==0.23.4

sudo -H pip3 install numpy==1.15.4

sudo -H pip3 install matplotlib==3.0.2
