import time
from scipy.optimize import minimize

def mean_squared_error(x, locations, distances):
	mse = 0.0
	for loca, dist in zip(locations, distances):
		dist_calc = ((x[0]-loca[0])**2 + (x[1] - loca[1])**2)**0.5
		mse += (dist_calc + dist)**2 
	return mse / len(distances)

class Localizer:
	def __init__(self, initial_x, initial_y, out_file = None):
		self.start_time = time.time()
		self.history = list()
		self.in_meas_interval = False
		self.measurements = dict()
		self.x = initial_x
		self.y = initial_y
		self.out_file = out_file
		if self.out_file != None:
			with open(self.out_file, "a") as ofile:
				ofile.write('new run\ntime(ms),x(m),y(m)\n')
		
	def start_meas_interval(self):
		self.measurements = dict()
		self.in_meas_interval = True
		
	def add_Meas(self, landmark_id, landmark_x, landmark_y, distance):
		if not self.in_meas_interval:
			return
		elif landmark_id in self.measurements:
			self.measurements[landmark_id][2] = (self.measurements[landmark_id][2] + distance)/2
		else:
			self.measurements[landmark_id] = [landmark_x, landmark_y, distance]
		
	def compute_location(self):
		locations = list()
		distances = list()
		for val in self.measurements.values():
			locations.append((val[0], val[1]))
			distances.append(val[2])
			
		result = minimize(
		mean_squared_error,
		(self.x, self.y),
		args=(locations, distances),
		method='L-BFGS-B',
		options={
			'ftol':1e-5,
			'maxiter':1e+7
		})
		
		self.history.append((time.time() - self.start_time, result.x))
		self.x = result.x[0]
		self.y = result.x[1]
		print(result.x)
		if self.out_file != None:
			with open(self.out_file, "a") as ofile:
				ofile.write(str(self.history[-1][0]) + "," + str(self.history[-1][1][0]) + "," + str(self.history[-1][1][1]) + "\n")
		
	def end_meas_interval(self):
		self.in_meas_interval = False