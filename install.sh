#!/bin/sh


echo Installing Active installer 2023 version 0.2.1

echo "[o] Note: this requires root permission"
echo "[*] It is ok to see some errors"

# git installation
sudo apt install git
sudo pacman -S git
sudo dnf install git
sudo yum install git
sudo zypper in git
sudo pkg install git
sudo pkg_add install git
sudo pkgin git


# installing python
sudo apt install python3
sudo pacman -S python3
sudo dnf install python3
sudo yum install python3
sudo zypper in python3
sudo pkg install python3
sudo pkg_add python3
sudo pkgin install python3
sudo pkg_add python3

# pciutils installation
sudo apt install pciutils
sudo dnf install pciutils
sudo yum install pciutils
sudo apk add pciutils-dev
sudo pkg install pciutils
sudo pkg_add sysutils/pciutils
sudo pkgin install pciutils


sudo mkdir /usr/src/rhenium
sudo mkdir /etc/rhenium

git clone https://github.com/Hussein-L-AlMadhachi/Rhenium.git
cd Rhenium


sudo cp ./rhenium.py /usr/src/rhenium
sudo cp ./ParserLib.py /usr/src/rhenium
sudo chmod +x /usr/src/rhenium/rhenium.py

sudo touch /etc/rhenium/SettingFile
lspci > HardwareInfo && sudo mv HardwareInfo /etc/rhenium
rm HardwareInfo

sudo cp run.py /usr/bin/rhenium
sudo chmod +x /usr/bin/rhenium
sudo cp run.py /usr/bin/renium
sudo chmod +x /usr/bin/renium

echo "[*] Active Installer installtion is completed"
echo "\nif you have seen any problems report them at \n    https://github.com/Hussein-L-AlMadhachi/Rhenium/issues\n"

sudo rhenium setup

cd ..
rm -rf Rhenium
