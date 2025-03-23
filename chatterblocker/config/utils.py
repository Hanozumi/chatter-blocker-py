'''
	chatter-blocker.config.py
	Configuration parser for chatter-blocker.

	Copyright (c) 2025 Hanozumi
'''

import csv

CONFIG_HEADER = '# Default config for chatter-blocker-py\n# Copyright (c) 2025 Hanozumi\n\n'

class Config:
	def __init__(self, c_char: str, delimiter: str):
		self.__c_char__ = c_char
		self.__delimiter__ = delimiter
		self.device = ''
		self.threshold = -1
		self.exclude_keys = []

	def read(self, path: str):
		with open(path) as conf:
			conf_raw = []
			for row in conf:
				raw = row.split(self.__c_char__)[0].strip()
				if raw != '': conf_raw.append(raw)

			for line in csv.reader(conf_raw, delimiter=self.__delimiter__):
				filtered = list(filter(lambda x: x.strip(), line))
				match filtered[0]:
					case 'device': self.device = filtered[1]
					case 'threshold': self.threshold = int(filtered[1])
					case 'exclude': self.exclude_keys = [e.strip() for e in filtered[1].split(',')] if len(filtered) > 1 else []
					case _: print(f'Unknown configuration option "{filtered[0]}"')

		if self.device == '': raise ValueError(f'A device needs to be specified in {path}.')
		if self.threshold <= 0: raise ValueError('Threshold value cannot be less than 1.')

	def write(self, path: str, data: dict):
		with open(path, 'w+') as config:
			config.write(CONFIG_HEADER)
			for key in data:
				config.write(f'{key}{self.__delimiter__}{data[key]}\n')