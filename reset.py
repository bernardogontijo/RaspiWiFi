
import subprocess
import fileinput
import os
import sys

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


print("Updating config files and copying them...")
update_config_paths()
os.system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
os.system('rm -f ./tmp/*')
os.system('sudo cp -r ./Reset\ Device/static_files/dhcpd.conf /etc/dhcp/')
os.system('sudo cp -r ./Reset\ Device/static_files/hostapd.conf /etc/hostapd/')
os.system('sudo cp -r ./Reset\ Device/static_files/interfaces.aphost /etc/network/interfaces')
os.system('sudo cp -r ./Reset\ Device/static_files/isc-dhcp-server.aphost /etc/default/isc-dhcp-server')
os.system('sudo cp -r ./Reset\ Device/static_files/rc.local.aphost /etc/rc.local')
print("Done")
