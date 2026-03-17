#!/bin/bash
# Script de configuración automática para Colab
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y xserver-xorg-core xserver-xorg-video-dummy x11-xserver-utils xterm openbox git xfce4 plank firefox unrar p7zip-full engrampa

# Instalación de Sunshine
wget -q https://github.com/LizardByte/Sunshine/releases/download/v0.21.0/sunshine-ubuntu-22.04-amd64.deb
sudo apt-get install -y ./sunshine-ubuntu-22.04-amd64.deb

# Configuración de video y arranque
mkdir -p /root/.config/sunshine
cp sunshine.conf /root/.config/sunshine/sunshine.conf
echo "video_codec = 1" >> /root/.config/sunshine/sunshine.conf

# Lanzar servicios
sudo nvidia-xconfig -a --allow-empty-initial-configuration --virtual=1280x720 --busid PCI:0:4:0
nohup sudo Xorg :1 -seat seat-1 -allowMouseOpenFail -novtswitch -nolisten tcp > /dev/null 2>&1 &
sleep 3
DISPLAY=:1 xsetroot -solid '#3355ff'
su - user -c "DISPLAY=:1 nohup startxfce4 > /dev/null 2>&1 &"
DISPLAY=:1 nohup sunshine /root/.config/sunshine/sunshine.conf > sunshine.log 2>&1 &
