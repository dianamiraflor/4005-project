"""
facility.py is the main module of the simulation. It contains an environment, Facilitiy and processes defined by generators.
Such processes are the two inspectors and three workstations. 

Running this module will begin the project's simulation.

Author: Diana Miraflor
Carleton University
"""

import simpy
import service_times
import random
from math import sqrt
from scipy.stats import t, norm as z
from constants import *

# Get all the service times of inspectors and workstations
st = service_times.ServiceTimes()
startTime=5000

class Facility: 
	"""
	A Facility class.
	Contains the 5 buffers shared between the inspectors and workstations, as well as containers for inspectors to fetch
	components from.
	"""
	def __init__(self, env):
		self.env=env

		self.containers={
			# Instantiate the containers for loading the components for inspectors
			'c1':simpy.Container(env, capacity=c1_max, init=c1_initial),
			'c2':simpy.Container(env, capacity=c2_max, init=c2_initial),
			'c3':simpy.Container(env, capacity=c3_max, init=c3_initial),

			# Instantiate the containers for output
			'p1':simpy.Container(env, capacity=c1_max, init=0),
			'p2':simpy.Container(env, capacity=c1_max, init=0),
			'p3':simpy.Container(env, capacity=c1_max, init=0),

			# Instantiate the containers (buffers) for each workstation
			'c1w1':simpy.Container(env, capacity=buffer_capacity),
			'c1w2':simpy.Container(env, capacity=buffer_capacity),
			'c1w3':simpy.Container(env, capacity=buffer_capacity),
			'c2w2':simpy.Container(env, capacity=buffer_capacity),
			'c3w3':simpy.Container(env, capacity=buffer_capacity)
		}

		self.total_times={
			'i1':[],
			'i22':[],
			'i23':[],
			'w1':[],
			'w2':[],
			'w3':[]
		}
		self.service_times={
			'i1':[],
			'i22':[],
			'i23':[],
			'w1':[],
			'w2':[],
			'w3':[]
		}
		self.idle_times={
			'i1':[],
			'i22':[],
			'i23':[],
			'w1':[],
			'w2':[],
			'w3':[]
		}

	def get_employees(self):
		employees={
			"i1":Employee(self.env, self, "i1",
						  ["c1"],
						  ["c1w1", "c1w2", "c1w3"]),
			"i2":Employee(self.env, self, "i2",
						  ["c2", "c3"],
						  ["c2w2", "c3w3"]),
			"w1":Employee(self.env, self, "w1",
						  ["c1w1"],
						  ["p1"]),
			"w2":Employee(self.env, self, "w2",
						  ["c1w2", "c2w2"],
						  ["p2"]),
			"w3":Employee(self.env, self, "w3",
						  ["c1w3", "c3w3"],
						  ["p3"])
		}

		return employees

	def print_levels(self):
		c1=self.containers["c1"].level
		c2=self.containers["c2"].level
		c3=self.containers["c3"].level

		p1=self.containers["p1"].level
		p2=self.containers["p2"].level
		p3=self.containers["p3"].level

		c1w1=self.containers["c1w1"].level
		c1w2=self.containers["c1w2"].level
		c1w3=self.containers["c1w3"].level
		c2w2=self.containers["c2w2"].level
		c3w3=self.containers["c3w3"].level

		print("\nContainer Levels")
		print(f"C1: {c1}\tC2: {c2}\tC3: {c3}")
		print(f"C1W1: {c1w1}\tC1W2: {c1w2}\tC1W3: {c1w3}\tC2W2: {c2w2}\tC3W3: {c3w3}")
		print(f"P1: {p1}\tP2: {p2}\tP3: {p3}")

class Employee:
	def __init__(self, env, facility, name, ins, outs):
		self.env=env
		self.facility=facility
		self.name=name
		self.ins=ins
		self.outs=outs
		if "i" in name:
			self.inspector=True
			self.workstation=False
		else:
			self.inspector=False
			self.workstation=True

	def run(self):
		facility=self.facility
		env=self.env

		while True:
			input_request=None
			output_request=None
			in_str=""
			out_str=""
			# special_index is used to handle i2 which has two indecies: i22 & i23
			special_index=self.name

			start_time=env.now

			# Pick the input and output containers for an inspector
			if self.inspector:
				# Request one input
				input_name=random.choice(self.ins)
				input=facility.containers[input_name]
				input_request=input.get(1)
				in_str=input_name

				# Set special index if appropriate
				if self.name=="i2":
					special_index+=in_str[1]

				# Choose an output that has an appropriate component type and the shortest queue
				output_name=random.choice([element for element in self.outs if input_name in element])
				if self.name=="i1":
					output_name=self.get_chosen_buffer()
				output=facility.containers[output_name]
				output_request=output.put(1)
				out_str=output_name

				print(f"{env.now:.2f}:\t\t{self.name} inspecting {input_name}")

			# Pick the input and output containers for a workstation
			elif self.workstation:
				# Request all inputs
				input_request_list=[]
				for input_name in self.ins:
					print(f"{env.now:.2f}:\t\t{self.name} requesting {input_name}")
					input_request_list.append(facility.containers[input_name].get(1))
				input_request=simpy.events.AllOf(env,input_request_list)
				in_str=str(self.ins)

				# There is only one output option
				output_name=self.outs[0]
				output=facility.containers[output_name]
				output_request=output.put(1)
				out_str=output_name

			service_time=st.get_random(special_index)
			time_request=env.timeout(service_time)

			# Do the actual requests
			yield input_request
			yield time_request
			yield output_request
			end_time=env.now
			total_time=end_time-start_time

			facility.total_times[special_index].append(total_time)
			facility.service_times[special_index].append(service_time)
			facility.idle_times[special_index].append(total_time-service_time)

			print(f"{env.now:.2f}:\t\t{self.name} placed {in_str} into {out_str} after {service_time:.2f} min")

	def get_chosen_buffer(self):
		"""
		A method for inspector 1 to pick the buffer with the shortest queue.
		"""
		c1w1=self.facility.containers["c1w1"].level
		c1w2=self.facility.containers["c1w2"].level
		c1w3=self.facility.containers["c1w3"].level

		if (c1w1<c1w2 and c1w1<c1w3) or (c1w1==c1w2==c1w3==2):
			return "c1w1"
		elif c1w2<c1w3:
			return "c1w2"
		elif c1w3<c1w2:
			return "c1w3"
		else:
			return random.choice(["c1w2","c1w3"])

def littles_law(duration=30000):
	env=simpy.Environment()
	facility=Facility(env)

	employees=facility.get_employees()

	for i in employees:
		env.process(employees[i].run())

	print(f'STARTING MANUFACTURING FACILITY SIMULATION')
	print(f'----------------------------------')
	env.run(until=duration)
	print(f'----------------------------------')
	print(f'SIMULATION COMPLETED')

	facility.print_levels()


def multiple_durations(replications, batches, batch_interval):
	keys=['i1',	'i22','i23','w1','w2','w3']

	ensemble_avg={}

	for duration in range (batch_interval,batches*batch_interval+1,batch_interval):
		multi_run_avgs={
			'i1':[],
			'i22':[],
			'i23':[],
			'w1':[],
			'w2':[],
			'w3':[]
		}
		for num in range(replications):
			env=simpy.Environment()
			facility=Facility(env)

			employees=facility.get_employees()

			for i in employees:
				env.process(employees[i].run())

			env.run(until=duration)

			single_run_avgs={}
			for key in keys:
				if len(facility.service_times[key])==0:
					single_run_avgs[key]=0
				else:
					single_run_avgs[key]=sum(facility.service_times[key])/len(facility.service_times[key])

				multi_run_avgs[key].append(single_run_avgs[key])

			# print(*single_run_avgs.values(), sep="\t")

		for key in keys:
			ensemble_avg[key]=sum(multi_run_avgs[key])/len(multi_run_avgs[key])
		ensemble_avg["time"]=duration
		print(*ensemble_avg.values(), sep="\t")

def multiple_replications(replications, duration):
	keys=['i1',	'i22','i23','w1','w2','w3']
	multi_run_avgs={
		'i1':[],
		'i22':[],
		'i23':[],
		'w1':[],
		'w2':[],
		'w3':[]
	}
	ensemble_avg={}
	sample_variance={}
	confidence_interval={}
	r_val={}


	for num in range(replications):
		env=simpy.Environment()
		facility=Facility(env)

		employees=facility.get_employees()

		for i in employees:
			env.process(employees[i].run())

		env.run(until=duration)

		single_run_avgs={}
		for key in keys:
			if len(facility.service_times[key])==0:
				single_run_avgs[key]=0
			else:
				single_run_avgs[key]=sum(facility.service_times[key])/len(facility.service_times[key])

			multi_run_avgs[key].append(single_run_avgs[key])

		print(*single_run_avgs.values(), sep="\t")

	for key in keys:
		ensemble_avg[key]=sum(multi_run_avgs[key])/len(multi_run_avgs[key])

		tmp_sum=0
		for yi in multi_run_avgs[key]:
			tmp_sum+=(yi-ensemble_avg[key])**2

		sample_variance[key]=1/(replications-1) * tmp_sum

		# Scores for 95% confidence
		t_score=t.ppf(0.975,df=replications-1)
		z_score=z.ppf(0.975)

		confidence_interval[key]=t_score*sqrt(sample_variance[key]/replications)

		r_val[key]=((z_score**2)*sample_variance[key])/0.2

	print("\nT-score:")
	print(t_score)

	print("\nSample Variances:")
	print(*[format(value, ".2f") for value in sample_variance.values()], sep="\t")

	print("\nStandard Deviation:")
	print(*[format(sqrt(value), ".2f") for value in sample_variance.values()], sep="\t")

	print("\nMeans:")
	print(*[format(value, ".2f") for value in ensemble_avg.values()], sep="\t")

	print("\nCI (+/-):")
	print(*[format(value, ".2f") for value in confidence_interval.values()], sep="\t")

	print(f"\nR at {replications} replications:")
	print(*[format(value, ".2f") for value in r_val.values()], sep="\t")

def normal(duration=30000):
	env=simpy.Environment()
	facility=Facility(env)

	employees=facility.get_employees()

	for i in employees:
		env.process(employees[i].run())

	print(f'STARTING MANUFACTURING FACILITY SIMULATION')
	print(f'----------------------------------')
	env.run(until=duration)
	print(f'----------------------------------')
	print(f'SIMULATION COMPLETED')

	facility.print_levels()

if __name__ == '__main__':
	"""
	THE MAIN METHOD.
	Run facility.py to start simulation.
	"""
	normal(30000)
	# multiple_durations(100,50,500)
	# multiple_replications(100,30000)
	# littles_law()