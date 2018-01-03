import RPi.GPIO as GPIO
import os
import subprocess
import fileinput
import sys
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0

def update_config_paths():
	project_path = os.path.dirname(os.path.abspath(__file__))
	os.system('sudo cp -a Reset\ Device/static_files/rc.local.aphost.template Reset\ Device/static_files/rc.local.aphost')
	os.system('sudo cp -a Reset\ Device/static_files/rc.local.apclient.template Reset\ Device/static_files/rc.local.apclient')
	os.system('sudo cp -a Reset\ Device/reset.py.template Reset\ Device/reset.py')

	with fileinput.FileInput("Reset Device/static_files/rc.local.aphost", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close

	with fileinput.FileInput("Reset Device/static_files/rc.local.apclient", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close

	with fileinput.FileInput("Reset Device/reset.py", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close

while True:
    while GPIO.input(18) == 1:
        time.sleep(1)
        counter = counter + 1

        print(counter)

        if counter == 9:
            print("Reset")
            update_config_paths()
            os.system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
            os.system('rm -f ./tmp/*')
            os.system('sudo cp -r ./Reset\ Device/static_files/dhcpd.conf /etc/dhcp/')
            os.system('sudo cp -r ./Reset\ Device/static_files/hostapd.conf /etc/hostapd/')
            os.system('sudo cp -r ./Reset\ Device/static_files/interfaces.aphost /etc/network/interfaces')
            os.system('sudo cp -r ./Reset\ Device/static_files/isc-dhcp-server.aphost /etc/default/isc-dhcp-server')
            os.system('sudo cp -r ./Reset\ Device/static_files/rc.local.aphost /etc/rc.local')
            print("Done. Now reboot")
            time.sleep(1)
            os.system('sudo reboot')
            

        if GPIO.input(18) == 0:
            counter = 0
            break

    time.sleep(1)
