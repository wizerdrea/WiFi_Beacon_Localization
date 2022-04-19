import pyshark
import subprocess
import json

#number of packets to sniff per channel before switching
#Note this will include useless packets from unknown access points
NUM_PACKETS = 12

#put pi into monitor mode
subprocess.run("sudo iw phy phy0 interface add mon0 type monitor", shell=True)
subprocess.run("sudo iw dev mon0 set channel 1", shell=True)
subprocess.run("sudo ifconfig mon0 up", shell=True)

# filter non-beacon frames
capture = pyshark.LiveCapture(interface='mon0', bpf_filter='wlan[0] == 0x80')

with open("beacon_map.json", "r") as file:
	beacon_map = json.load(file)

def print_frame_data(frame):
    if packet.wlan.bssid in beacon_map:
        print("In map")
        print(frame.wlan.bssid)
        print(frame.wlan_radio.signal_dbm)
        print(beacon_map[frame.wlan.bssid]["message"])
        
    else:
        print("Not in map:", frame.wlan.bssid, frame.wlan_radio.signal_dbm)

print('capture mode')

while(True):
	for packet in capture.sniff_continuously(packet_count=NUM_PACKETS):
        print_frame_data(packet)
			
	subprocess.run("sudo iw dev mon0 set channel 6", shell=True)

	for packet in capture.sniff_continuously(packet_count=NUM_PACKETS):
		print_frame_data(packet)
			
	subprocess.run("sudo iw dev mon0 set channel 11", shell=True)
			
	for packet in capture.sniff_continuously(packet_count=NUM_PACKETS):
        print_frame_data(packet)
			
	subprocess.run("sudo iw dev mon0 set channel 1", shell=True)
