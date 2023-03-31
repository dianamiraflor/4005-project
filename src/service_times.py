"""
service_times.py contains a class that outputs a random service time for the simulation. 

Author: Diana Miraflor
Carleton University
"""

import random
from constants import data_directory

class ServiceTimes():
	def __init__(self):
		self.times={}

		self.times["i1"]= self.file_reader("servinsp1.dat")
		self.times["i22"]=self.file_reader("servinsp22.dat")
		self.times["i23"]=self.file_reader("servinsp23.dat")
		self.times["w1"]= self.file_reader("ws1.dat")
		self.times["w2"]= self.file_reader("ws2.dat")
		self.times["w3"]= self.file_reader("ws3.dat")

	def get_random(self, name) -> float:
		"""
		Takes in the name of the inspector/ workstation and returns a randomly selected service time
		"""
		return random.choice(self.times[name])

	def file_reader(self, fname):
		"""
		Takes in a filename and returns an array of the service times contained in the file
		"""
		st=[]
		data=data_directory/fname
		with open(data, 'r') as f:
			for line in f.readlines():
				st.append(float(line))

		return st

