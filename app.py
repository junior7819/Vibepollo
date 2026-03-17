import os
import glob
import subprocess
import sys
import time
import pwd
import re
from tqdm.notebook import tqdm

# --- INTEGRACIÓN VIBEPOLLO ---
# Añadimos la ruta de tu proyecto al sistema para que reconozca tus ejecutables
os.environ["PATH"] += ":/usr/games:/usr/lib/games:/content/Vibepollo"

def no_traceback(exctype, value, tb):
    print("⚠️ Error detectado. Intentando continuar...")
sys.excepthook = no_traceback

def run(cmd):
    subprocess.run(
        cmd, shell=True, check=True, text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def optional_input(prompt, default="n"):
    try: return input(prompt).strip().lower() or default
    except: return default

def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError: return False

def backup_user():
    if not os.path.ismount("/content/drive"):
        print("⚠️ Drive no montado. Saltando backup.")
        return
    ans = optional_input("💾 ¿Querés respaldar /home/user en Drive? (y/n): ", "n")
    if ans == "y":
        run("pkill -KILL -u user || true")
        src, dst = "/home/user", "/content/drive/MyDrive/backup.tar.gz"
        print(f"⏳ Creando backup en Drive...")
        tar = subprocess.Popen(["tar","-cf","-","-C",src,"--exclude=Downloads","--exclude=.config","."], stdout=subprocess.PIPE)
        pigz = subprocess.Popen(["pigz","-9"], stdin=tar.stdout, stdout=open(dst,"wb"))
        tar.stdout.close(); tar.wait(); pigz.wait()
        print("🎉 Backup completado.")

def restore_backup():
    if not os.path.ismount("/content/drive") or not os.path.exists("/content/drive/MyDrive/backup.tar.gz"):
        return
    print("⏳ Restaurando backup de Drive...")
    run("echo 'root:123456' | sudo chpasswd")
    if not user_exists("user"):
        run("sudo useradd -m user && echo 'user:123456' | sudo chpasswd && usermod -aG sudo user")
    run("pigz -dc /content/drive/MyDrive/backup.tar.gz | tar -xf - -C /home/user")
    run("sudo chown -R user:user /home/user")

def main():
    print("🚀 Iniciando Motor Vibepollo (Basado en Colab Cloud Gaming)")
    
    # 1. Montaje de Drive para persistencia
    if not os.path.ismount("/content/drive"):
        try:
            from google.colab import drive
            drive.mount("/content/drive", force_remount=True)
        except: print("⚠️ No se pudo montar Drive.")

    # 2. Instalación de paquetes desde el Backup (Cuerpo del Sistema)
    if not os.path.exists("/packages"):
        print("📦 Descargando e instalando backup de programas...")
        run("wget -qO- https://github.com/OkamuraYuji/Colab-Gaming/releases/download/1.0.0/packages.tar.gz | pigz -dc | tar -xv -C /")
        # Configuramos el PATH permanentemente
        run("echo '#!/bin/sh\nexport PATH=\"$PATH:/usr/games:/usr/lib/games:/content/Vibepollo\"' | sudo tee /etc/profile.d/custom_path.sh > /dev/null && sudo chmod +x /etc/profile.d/custom_path.sh")
        # Tailscale
        run("curl -L https://pkgs.tailscale.com/stable/tailscale_1.94.2_amd64.tgz | sudo tar --strip-components=1 -xzv -C /usr/local/bin")
        run("mkdir -p /var/lib/tailscale")
        run("nohup tailscaled --tun=userspace-networking --socket=/run/tailscale/tailscaled.sock &")

    # 3. Red y Backup
    !tailscale up
    ip = subprocess.check_output("tailscale ip -4", shell=True, text=True).strip()
    print(f"🌐 Tu IP de Tailscale es: {ip}")
    
    if os.path.exists("/content/drive/MyDrive/backup.tar.gz"):
        if optional_input("💾 ¿Restaurar archivos anteriores? (y/n): ", "y") == "y":
            restore_backup()

    # 4. Drivers y Gráficos
    print("🎮 Configurando drivers NVIDIA y Servidor X...")
    run("chmod +x /packages/NVIDIA*.run && echo 1 | /packages/NVIDIA*.run --no-kernel-module --ui=none")
    run("nvidia-xconfig -a --allow-empty-initial-configuration --virtual=1920x1080 --busid PCI:0:4:0")
    run("nohup sudo Xorg :1 -seat seat-1 -allowMouseOpenFail -novtswitch -nolisten tcp &")
    time.sleep(2)
    run("DISPLAY=:1 xhost +local:")

    # 5. Lanzamiento del Escritorio y Sunshine
    print("🖥️ Levantando entorno gráfico...")
    run("cp /packages/wallpaper.jpg /home/user/ 2>/dev/null || true")
    run("su - user -c \"nohup pulseaudio --exit-idle-time=-1 &\"")
    run("su - user -c \"DISPLAY=:1 nohup startxfce4 &\"") # Cambiado a XFCE que es el de tu backup
    run("su - user -c \"rm -rf ~/.config/sunshine ; DISPLAY=:1 nohup sunshine &\"")

    # 6. Interfaz Web para el PIN (Flask)
    from flask import Flask, request, render_template_string
    import threading
    app = Flask(__name__)
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            pin = request.form['pin'].strip()
            run(f'curl -u admin:admin -X POST -k https://localhost:47990/api/password -H "Content-Type: application/json" -d \'{{"currentUsername":"admin","currentPassword":"admin","newUsername":"admin","newPassword":"admin","confirmNewPassword":"admin"}}\'')
            run(f'curl -u admin:admin -X POST -k https://localhost:47990/api/pin -H "Content-Type: application/json" -d \'{{"pin":"{pin}","name":"Vibepollo-Device"}}\'')
            return "✅ PIN ENVIADO CORRECTAMENTE"
        return f'<html><body style="background:#111;color:white;text-align:center;padding-top:50px;"><h2>🔑 PIN Moonlight</h2><form method="post"><input type="text" name="pin" placeholder="****" style="font-size:24px;width:100px;text-align:center;"><br><br><button type="submit" style="padding:10px 20px;">Vincular</button></form></body></html>'

    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=3000), daemon=True).start()
    print(f"🔗 Vinculación PIN: http://{ip}:3000")

    print("✅ TODO LISTO. El sistema seguirá activo hasta que cierres Colab.")
    while True: time.sleep(100)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: backup_user()
