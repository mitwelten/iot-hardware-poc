# APGateway
## Setup
### Prepare SD Card
On the computer
- Install [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
- Select _Raspberry Pi OS (other)_ > _Raspberry Pi OS Lite (32-bit)_
- Click _Choose SD Card_, then _Write_
- Remove, re-insert SD Card
- To enable SSH, type
    ```
    $ touch /Volumes/boot/ssh
    ```

### Prepare Raspberry Pi 4B
On the Pi
- Insert prepared SD Card
- Connect to power via USB-C
- Connect to Ethernet via RJ45
- Add Argon Poly+ case with fan

On the computer
- Share Computer Wi-Fi to Ethernet
- Log into Pi via SSH (pw: raspberry)
    ```
    $ ssh pi@raspberrypi.local
    ```

On the Pi
- Change the password
    ```
    $ passwd
    ```
- Note the MAC address
    ```
    $ ifconfig | grep ether
    ```
- Expand the filesystem
    ```
    $ sudo raspi-config # Advanced Options > Expand Filesystem
    ```
- Enable the fan
    ```
    $ sudo nano /boot/config.txt
    ...
    dtoverlay=gpio-fan,gpiopin=18,temp=55000
    ```
- Format and mount the hard disk (based on [this](https://www.raspberrypi.org/documentation/configuration/external-storage.md))
    ```bash
    sudo apt update
    sudo apt install -y btrfs-progs # for BTRFS
    sudo blkid # identify the device (i.e. /dev/sda)
    sudo mkfs.btrfs -L capture /dev/sda1 # matching the device identified in previous step
    echo '/dev/disk/by-label/capture /mnt/elements btrfs   defaults,auto,user    0 0' | sudo tee --append /etc/fstab
    sudo mount /mnt/elements
    sudo chown pi /mnt/elements
    ```
- Install nmap
    ```
    $ sudo apt-get install nmap
    ```
- Install capture.py & .service
    ```
    $ cd ~
    $ mkdir capture
    $ cd capture
    $ wget -O capture.py https://raw.githubusercontent.com/mitwelten/mitwelten-iot-hardware-poc/main/RaspberryPi/APGateway/Capture/capture.py
    $ wget -O config.json https://raw.githubusercontent.com/mitwelten/mitwelten-iot-hardware-poc/main/RaspberryPi/APGateway/Capture/config.json
    $ nano config.json # edit camera_ids
    $ sudo wget -O /etc/systemd/system/capture.service https://raw.githubusercontent.com/mitwelten/mitwelten-iot-hardware-poc/main/RaspberryPi/APGateway/Capture/capture.service
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable capture.service
    $ sudo systemctl start capture.service
    ```
- [Install Yaler](https://yaler.net/raspberrypi) (or an [alternative](https://alternativeto.net/software/yaler/)) and enable [SSH access](https://yaler.net/raspberrypi#SSH)
- Make sure the daemons are up and running
    ```
    $ ps aux | grep [c]apture
    $ ps aux | grep [y]aler
    ```
