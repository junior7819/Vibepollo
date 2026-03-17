#!/bin/bash
# ==========================================
# Setup Integral - Vibepollo (Colab Edition)
# ==========================================

echo "🔄 1. Actualizando y eliminando bloqueos..."
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --fix-broken

echo "🖥️ 2. Instalando Infraestructura Gráfica y Escritorio..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    xserver-xorg-core xserver-xorg-video-dummy x11-xserver-utils \
    xfce4 xfce4-terminal openbox git

echo "🛰️ 3. Instalando Sunshine Oficial..."
wget -q https://github.com/LizardByte/Sunshine/releases/download/v0.21.0/sunshine-ubuntu-22.04-amd64.deb
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y ./sunshine-ubuntu-22.04-amd64.deb

echo "🌐 4. Instalando Apps (Firefox, Plank, Extractores)..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    firefox plank unrar p7zip-full engrampa

echo "⚙️ 5. Configurando Sunshine y GPU..."
mkdir -p /root/.config/sunshine
# Si el archivo sunshine.conf existe en el repo, lo usamos, si no, creamos uno base
if [ -f "sunshine.conf" ]; then
    cp sunshine.conf /root/.config/sunshine/sunshine.conf
else
    echo "video_codec = 1" > /root/.config/sunshine/sunshine.conf
fi
echo "video_codec = 1" >> /root/.config/sunshine/sunshine.conf

echo "🚀 6. Lanzando Servicios..."
sudo nvidia-xconfig -a --allow-empty-initial-configuration --virtual=1280x720 --busid PCI:0:4:0
nohup sudo Xorg :1 -seat seat-1 -allowMouseOpenFail -novtswitch -nolisten tcp > /dev/null 2>&1 &
sleep 3
DISPLAY=:1 xsetroot -solid '#3355ff'
su - user -c "DISPLAY=:1 nohup startxfce4 > /dev/null 2>&1 &"
su - user -c "DISPLAY=:1 nohup plank > /dev/null 2>&1 &"
DISPLAY=:1 nohup sunshine /root/.config/sunshine/sunshine.conf > sunshine.log 2>&1 &

echo "✅ ¡PROCESO FINALIZADO! Conecta Moonlight ahora."
