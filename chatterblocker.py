'''
	chatter-blocker.py
	Python implementation of a chatter blocker (e.g. for mechanical keyboard chatter). 

	Copyright (c) 2025 Hanozumi
'''

import os
import libevdev
from pick import pick
from pathlib import Path
from chatterblocker.config import Config

os.chdir(os.path.dirname(__file__))

available_devices = list(filter(lambda x: x.endswith('event-kbd'), os.listdir('/dev/input/by-id/')))

# for event_kbd in list(filter(lambda x: x.endswith('event-kbd'), os.listdir('/dev/input/by-id/'))):
# 	print(os.path.realpath(os.path.join('/dev/input/by-id/', event_kbd)))

config = Config('#', '=')

config_path = Path.home() / '.config/chatterblocker.conf'
if not os.path.isfile(config_path):
	config_data = {
		'device': pick(available_devices, 'Select input device:')[0],
		'threshold': int(input('Select max input threshold in ms: ')),
		'exclude': ''
	}
	config.write(config_path, config_data)