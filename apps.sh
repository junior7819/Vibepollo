#!/bin/bash

echo "🚀 Entorno Vibepollo detectado."
echo "📦 Usando aplicaciones pre-instaladas del backup..."

# Dar permisos de ejecución a los binarios en tu carpeta por si acaso
chmod +x /content/Vibepollo/* 2>/dev/null

# Aquí podés poner comandos que quieras que se ejecuten al inicio 
# sin instalar nada, como crear una carpeta de partidas:
mkdir -p /home/user/Partidas_PES

echo "✅ Configuración de inicio finalizada."
