#!/usr/bin/env python
from dji_sdk.dji_drone import DJIDrone
import dji_sdk.msg 
import requests
import time
import sys
import math
import json
def main():
	drone = DJIDrone()
	while True:
		time.sleep(1);
		payload = {'query': 'ask','compass': drone.compass,	'global_position': drone.global_position, 'global_position_ref': drone.global_position_ref, 'local_positon':drone.local_position, 'local_positon_ref':drone.local_position_ref, 'power_status': drone.power_status, 'time_stamp' : drone.time_stamp, 'flight_control_info': drone.flight_control_info}
		r = requests.get('https://script.google.com/macros/s/AKfycby4M1Po83RuAME17YcnDq9C-O4lsXmqK2fEZ7uVhFA1QPOd-A3a/exec',payload);
		print r.text	
		if(r.text.find("action") != -1):	
			
			command = r.json()["command"]
			
			if(json.loads(command)["action"] == "localNavigation"):
				x = int(json.loads(command)["x"])
				y = int(json.loads(command)["y"])
				z = int(json.loads(command)["z"])
				drone.local_position_navigation_send_request(x, y, z)

			if(json.loads(command)["action"] == "globalNavigation"):
				globlat1 = float(json.loads(command)["globlat1"])
				globlon1 = float(json.loads(command)["globlon1"])
				globalt1 = float(json.loads(command)["globalt1"])
				drone.global_position_navigation_send_request(globlat1, globlon1, globalt1)
			
			if(json.loads(command)["action"] == "testCircle"):
				drone.takeoff()
				time.sleep(5)
				R = int(json.loads(command)["r"])
				V = int(json.loads(command)["v"])
				print R
				print V
				for i in range(300):
					vx = V * math.sin((V/R)*i/50.0)
					vy = V * math.cos((V/R)*i/50.0)
					drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, vx, vy, 0, 0)
					time.sleep(0.02)
				time.sleep(1)
				drone.landing()

			if(json.loads(command)["action"] == "waypoints"):
				lat1 = float(json.loads(command)["lat1"])
				lon1 = float(json.loads(command)["lon1"])
				alt1 = float(json.loads(command)["alt1"])
				stay1 = float(json.loads(command)["stay1"])
				lat2 = float(json.loads(command)["lat2"])
				lon2 = float(json.loads(command)["lon2"])
				alt2 = float(json.loads(command)["alt2"])
				stay2 = float(json.loads(command)["stay2"])
				newWaypointList = [
				dji_sdk.msg.Waypoint(latitude = lat1, longitude = lon1, altitude = alt1, staytime = stay1, heading = 0),
				dji_sdk.msg.Waypoint(latitude = lat2, longitude = lon2, altitude = alt2, staytime = stay2, heading = 90)]
				drone.waypoint_navigation_send_request(newWaypointList)
				
			if(json.loads(command)["action"] == "request_control"):
				drone.request_sdk_permission_control()
				time.sleep(1)

			if(json.loads(command)["action"] == "release_control"):
				drone.release_sdk_permission_control()
				time.sleep(1)

			if(json.loads(command)["action"] == "takeoff_mission"):
				drone.takeoff()
				time.sleep(2)

			if(json.loads(command)["action"] == "landing_mission"):
				drone.landing()
				time.sleep(2)
			
			if(json.loads(command)["action"] == "testAttitude"):
				drone.takeoff()
				time.sleep(5)
				for i in range(100):
					if i < 90:
						drone.attitude_control(0x40, 0, 2, 0, 0)
					else:
						drone.attitude_control(0x40, 0, 0, 0, 0)
					time.sleep(0.02)
				time.sleep(1)
				for i in range(200):
					if i < 180:
						drone.attitude_control(0x40, 2, 0, 0, 0)
					else:
						drone.attitude_control(0x40, 0, 0, 0, 0)
					time.sleep(0.02)
				time.sleep(1)


				for i in range(200):
					if i < 180:
						drone.attitude_control(0x40, -2, 0, 0, 0)
					else:
						drone.attitude_control(0x40, 0, 0, 0, 0)
					time.sleep(0.02)
				time.sleep(1)

				for i in range(200):
					if i < 180:
						drone.attitude_control(0x40, 0, 2, 0, 0)
					else:
						drone.attitude_control(0x40, 0, 0, 0, 0)
					time.sleep(0.02)
				time.sleep(1)

				for i in range(200):
					if i < 180:
						drone.attitude_control(0x40, 0, -2, 0, 0)
					else:
						drone.attitude_control(0x40, 0, 0, 0, 0)
					time.sleep(0.02)
				time.sleep(1)

				for i in range(200):
					if i < 180:
						drone.attitude_control(0x40, 0, 0, 0.5, 0)
					else:
						drone.attitude_control(0x40, 0, 0, 0, 0)
					time.sleep(0.02)
				time.sleep(1)

				for i in range(200):
					if i < 180:
						drone.attitude_control(0x40, 0, 0, -0.5, 0)
					else:
						drone.attitude_control(0x40, 0, 0, 0, 0)
					time.sleep(0.02)
				time.sleep(1)

				for i in range(200):
					if i < 180:
						drone.attitude_control(0x40, 0, 0, 0, 90)
					else:
						drone.attitude_control(0x40, 0, 0, 0, 0)
					time.sleep(0.02)
				time.sleep(1)

				for i in range(200):
					if i < 180:
						drone.attitude_control(0x40, 0, 0, 0, -90)
					else:
						drone.attitude_control(0x40, 0, 0, 0, 0)
					time.sleep(0.02)
				time.sleep(1)

				drone.landing()

		print drone.activation
if __name__ == "__main__":
	main()		
