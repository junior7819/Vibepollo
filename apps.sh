#!/bin/bash

# 1. SOLUCIÓN DE PANTALLA
# Forzamos al sistema a que use todo el espacio disponible del monitor virtual
echo "🖥️ Ajustando resolución y expandiendo escritorio..."
DISPLAY=:1 xrandr --output DVI-D-0 --auto

# 2. CONFIGURACIÓN VIBEPOLLO
# Aseguramos que los scripts del repo tengan permisos de ejecución
echo "🚀 Configurando entorno Vibepollo..."
chmod +x /content/Vibepollo/*.py 2>/dev/null
chmod +x /content/Vibepollo/*.sh 2>/dev/null

# 3. PERSISTENCIA DE RUTA
# Agregamos Vibepollo al PATH del usuario para que los comandos funcionen siempre
if ! grep -q "Vibepollo" /home/user/.bashrc; then
    echo 'export PATH="$PATH:/content/Vibepollo"' >> /home/user/.bashrc
fi

echo "✅ Configuración finalizada. Pantalla corregida."

