#!/bin/bash

# Step 1: Install VNC server if not already installed (optional)
echo "Installing tightvncserver..."
sudo apt update
sudo apt install -y tightvncserver

# Step 2: Set a default screen resolution (if headless)
echo "Setting display resolution..."
sudo raspi-config nonint do_resolution 2 82  # 82 = 1920x1080, 2 = HDMI 1

# Step 3: Create a VNC password (skip if already configured)
echo "Creating VNC password..."
su - pi -c 'echo "raspberry" | vncpasswd -f > ~/.vnc/passwd'
su - pi -c 'chmod 600 ~/.vnc/passwd'

# Step 4: Create VNC autostart systemd service
echo "Creating systemd service for VNC..."
sudo tee /etc/systemd/system/vncserver.service > /dev/null <<EOF
[Unit]
Description=Start TightVNC server at boot
After=syslog.target network.target

[Service]
Type=forking
User=pi
PAMName=login
PIDFile=/home/pi/.vnc/%H:1.pid
ExecStart=/usr/bin/vncserver :1
ExecStop=/usr/bin/vncserver -kill :1

[Install]
WantedBy=multi-user.target
EOF

# Step 5: Enable and start the service
echo "Enabling and starting vncserver service..."
sudo systemctl daemon-reload
sudo systemctl enable vncserver.service
sudo systemctl start vncserver.service

echo "✅ VNC server setup complete. It will start automatically at boot."
