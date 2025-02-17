Added Systemd file start-server-pi.service that contains:

[Unit]
Description= Starts pi server on startup
After=network.target
[Service]
Type=idle
WorkingDirectory=/home/pi/CS190b/CS190B-SubtleReminder-qiru-max-chris/src/
ExecStart= python app.py
[Install]
WantedBy=multi-user.target


Testing the systemctl service:
sudo systemctl start start-server-pi.service

To stop service upon re-entry into PI:
sudo systemctl stop start-server-pi.service
NEEDS TO BE STOPPED EVERYTIME THE PI IS TURNED ON !
