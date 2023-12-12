#!/bin/sh

echo "Using Active installer 2023 version 0.2.1"

echo "[o] Note: this may require root permission"
echo "[*] It is ok to see some errors"

# git installation
sudo apt install git
sudo pacman -S git
sudo dnf install git
sudo yum install git
sudo zypper in git
sudo pkg install git
sudo pkg_add git
sudo pkgin update
sudo pkg_add git


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


echo "
import os
if os.path.isfile(\"/usr/bin/rhenium\"):
    os.system(\"rhenium install\")
else:
    os.system(\"git clone https://github.com/Hussein-L-AlMadhachi/Rhenium.git; cd Rhenium ; sh install.sh")
" > install.py


python3 install.py
rhenium install


rm install.py
rm -rf Rhenium

echo "[*] Installtion completed"
