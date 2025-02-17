# Feb 10, 2023 MAX:
	- Configured Pi to be used on home network by adding to wpa_supplicant
	- Setup Pi SSH Key and cloned our github repo onto Pi
	- Installed yarn on Pi
	- Setup breadboard with led and 220 ohm resistor connected to pi gpio 26
# Feb 17, 2023 MAX:
	- I wrote some basic LED python scripts for the pi
	- These include turning the LED on and off as well as breathing the LED
	- I also added some features in app.py that allows me to test these scripts from the actual site
	- I can now turn the led on and off as well as blink from the site
# Feb 24, 2023 MAX:
	- So I have begun adding boot instructions to the pi 
	- When the pi is turned on the server is started so users don't have to worry about starting the server on their own
	- I did this by editing the /etc/rc.local file and adding the yarn start-server command
	- I can kill the server by using using 'ps aux' and 'kill [pid]' of whatever pid the server is running on 
	- I also added a feature where the led blinks three times when the server runs
# March 2, 2023 MAX:
	- So I figured out that /etc/rc.local wouldn't start the server correctly so I looked into other solutions
	- I figured out that the server requires an internet connection so I would need to add a systemd file in /lib/systemd/system of the pi
	- I created a file start-server-pi.service that runs when the PI starts up, and starts the server
	- More info can be found in the systemd_instructions.md file in this directory 
# March 17, 2023 MAX:
	- I completed construction of the prototype box
	- I built a simple circuit and hooked everything up to the box prototype 