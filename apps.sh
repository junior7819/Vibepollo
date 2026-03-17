#!/bin/bash
# ==========================================
# Módulo de Aplicaciones - Vibepollo
# ==========================================

echo "🌐 Instalando Navegador Firefox..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y firefox

echo "🖥️ Instalando Barra de Aplicaciones (Plank)..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y plank

echo "🗜️ Instalando Soporte para RAR, 7Z y ZIP..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y unrar p7zip-full p7zip-rar zip unzip engrampa

echo "🚀 Iniciando Plank en el escritorio..."
# Esto hace que la barra aparezca automáticamente en Moonlight
su - user -c "DISPLAY=:1 nohup plank > /dev/null 2>&1 &"

# Crear carpeta de escritorio por si no existe y dar permisos
mkdir -p /home/user/Desktop
chown user:user /home/user/Desktop

echo "✅ Aplicaciones y herramientas listas."
