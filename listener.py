import pyshark
import subprocess
import json
import localizer

#Number of localizations calculations to make
NUM_LOCAL_CALC = 5

#number of packets to sniff per channel before switching
#Note this will include useless packets from unknown access points
NUM_PACKETS = 12

PATH_LOSS_EXPONENT = 2.1

#Put pi into monitor mode
subprocess.run("sudo iw phy phy0 interface add mon0 type monitor", shell=True)
subprocess.run("sudo iw dev mon0 set channel 1", shell=True)
subprocess.run("sudo ifconfig mon0 up", shell=True)

#set pyshark to filter out all non-beacon frames
capture = pyshark.LiveCapture(interface='mon0', bpf_filter='wlan[0] == 0x80')

with open("beacon_map.json", "r") as file:
	beacon_map = json.load(file)

# Note: this initial guess is just where the monitor we mostly used was.
# It was never changed even when we started the program at other points
locali = localizer.Localizer(13, 24, "test.csv")

# function to take in packet, determine whether it is in the map,
# if it is calculate distance to access point,
# and pass distance and access point location to localizer
def handel_packet(packet, localizer):
    if packet.wlan.bssid in beacon_map:
        distance = 10**((int(packet.wlan_radio.signal_dbm) - beacon_map[packet.wlan.bssid]["one_m_rssi"])/(-10*PATH_LOSS_EXPONENT))
        localizer.add_Meas(packet.wlan.bssid, beacon_map[packet.wlan.bssid]["x"], beacon_map[packet.wlan.bssid]["y"], distance)

print('capture mode')

for i in range(NUM_LOCAL_CALC):
	locali.start_meas_interval()
	
	for packet in capture.sniff_continuously(packet_count=NUM_PACKETS):
		handel_packet(packet, locali)
			
	subprocess.run("sudo iw dev mon0 set channel 6", shell=True)

	for packet in capture.sniff_continuously(packet_count=NUM_PACKETS):
		handel_packet(packet, locali)
			
	subprocess.run("sudo iw dev mon0 set channel 11", shell=True)
			
	for packet in capture.sniff_continuously(packet_count=NUM_PACKETS):
		handel_packet(packet, locali)
			
	subprocess.run("sudo iw dev mon0 set channel 1", shell=True)
	
	locali.compute_location()
	
	locali.end_meas_interval()
	
print(locali.history)
			

			
