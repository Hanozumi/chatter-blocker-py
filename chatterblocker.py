'''
	chatter-blocker.py
	Python implementation of a chatter blocker (e.g. for mechanical keyboard chatter). 

	Copyright (c) 2025 Hanozumi
'''

import os
import libevdev
from time import sleep
from pick import pick
from chatterblocker.config import Config

os.chdir(os.path.dirname(__file__))

keys_last_released = {  }
keys_pressed = {  }
available_devices = list(filter(lambda x: x.endswith('event-kbd'), os.listdir('/dev/input/by-id/')))

config = Config('#', '=')

config_path = '/etc/chatterblocker.conf'
if not os.path.isfile(config_path):
	config_data = {
		'device': pick(available_devices, 'Select input device:')[0],
		'threshold': int(input('Select max input threshold in ms: ')),
		'exclude': ''
	}
	config.write(config_path, config_data)

config.read(config_path)
device_path = os.path.realpath(os.path.join('/dev/input/by-id/', config.device))

sleep(1)

print(f':: Listening to {config.device} @ {config.threshold}ms\r')
print(':: Excluded Keys:\r')
print(config.exclude_keys)

with open(device_path, 'rb') as fd:
	device = libevdev.Device(fd)
	if not device.has(libevdev.EV_KEY.KEY_ENTER): raise IOError(f'{device_path} does not seem to be a keyboard.')
	
	device.grab()
	udevice = device.create_uinput_device()

	while True:
		for e in device.events():
			if e.matches(libevdev.EV_SYN) or e.matches(libevdev.EV_MSC): continue
			if not e.matches(libevdev.EV_KEY) or e.value > 1: udevice.send_events([e, libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)])
			if e.code in config.exclude_keys: udevice.send_events([e, libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)])
			# e.value = 0 => up; 1 = down; 2 = held
			if e.value == 0:
				if keys_pressed.get(e.code):
					keys_last_released[e.code] = e.sec * 1E6 + e.usec
					udevice.send_events([e, libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)])
					keys_pressed[e.code] = False
			if e.value == 1:
				if not keys_pressed.get(e.code):
					now = e.sec * 1E6 + e.usec
					if now - (keys_last_released.get(e.code) or 0) < (config.threshold*1E3): continue
					udevice.send_events([e, libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)])
					keys_pressed[e.code] = True