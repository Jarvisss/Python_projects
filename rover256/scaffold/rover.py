
GAME_MOVE_N = "N"
GAME_MOVE_S = "S"
GAME_MOVE_W = "W"
GAME_MOVE_E = "E"
class Rover:
	def __init__(self, x, y, planet):
		"""
		Initialises the rover
		"""
		self.x = x
		self.y = y
		self.battery = 100
		self.elevation = 0
		self.explored_num = 1

		# Constants
		self.radius = 3
		self.planet = planet
		self.initialize()
		pass

	def initialize(self):
		width = self.planet.get_width()
		self.planet.tiles[self.x * width + self.y].set_occupant(self)
	def calculate_explored_percentage(self):
		return int(self.explored_num / self.planet.tile_num * 100)


	def scan_shade(self):
		"""
		scan shade
		:return:
		"""
		x = self.x
		y = self.y
		width = self.planet.get_width()
		height = self.planet.get_height()
		for xx in range(-self.radius + 1, self.radius):
			row = x + xx
			if row < 0:
				row = row + height
			elif row >= height:
				row = row - height
			print("|", end="")
			for yy in range(-self.radius + 1, self.radius):
				col = y + yy
				if col < 0:
					col = col + width
				elif col >= width:
					col = col - width

				current_tile = self.planet.tiles[row * width + col]
				if current_tile.explored == False:
					current_tile.explored = True
					self.explored_num += 1
				if xx == 0 and yy == 0:
					print("H|", end='')
				else:
					if current_tile.shaded:
						print("#|", end='')
					else:
						print(" |", end='')
			print('')

	def scan_elevation(self):
		"""
		scan elevation
		:return:
		"""
		x = self.x
		y = self.y
		width = self.planet.get_width()
		height = self.planet.get_height()
		for xx in range(-self.radius + 1, self.radius):
			row = x + xx
			if row < 0:
				row = row + height
			elif row >= height:
				row = row - height
			print("|",end="")
			for yy in range(-self.radius + 1, self.radius):
				col = y + yy
				if col < 0:
					col = col + width
				elif col >= width:
					col = col - width

				current_tile = self.planet.tiles[row * width + col]
				if current_tile.explored == False:
					current_tile.explored = True
					self.explored_num += 1
				if xx == 0 and yy == 0:
					print("H|", end='')
				else:
					if current_tile.is_slope:
						if current_tile.elevation[0] == self.elevation:
							print("\\|", end='')
						elif current_tile.elevation[1] == self.elevation:
							print("/|", end='')
						elif current_tile.elevation[1] > self.elevation:
							print("+|", end='')
						elif current_tile.elevation[0] < self.elevation:
							print("-|", end='')
					else:
						delta_elevation = current_tile.elevation - self.elevation
						if delta_elevation < 0:
							print("-|", end='')
						elif delta_elevation > 0:
							print("+|", end='')
						else:
							print(" |", end='')
			print('')

	def output_stats(self):
		explored_percentage = self.calculate_explored_percentage()
		print("Explored: {0} %".format(explored_percentage))
		print("Battery: {0}/100".format(self.battery))

	def finish(self):
		explored_percentage = self.calculate_explored_percentage()
		print("You explored {0} % of {1}.".format(explored_percentage, self.planet.name))

	def move(self, direction, cycles):
		"""
		Moves the rover on the planet
		"""
		if self.battery<=0:
			return False
		else:

			width = self.planet.get_width()
			height = self.planet.get_height()
			target_x = self.x
			target_y = self.y
			for step in range(cycles):
				if self.battery<=0:
					break
				if direction == GAME_MOVE_N:
					target_x -= 1
					if(target_x <0):
						target_x += height
				elif direction == GAME_MOVE_S:
					target_x += 1
					if (target_x >= height):
						target_x -= height
				elif direction == GAME_MOVE_W:
					target_y -= 1
					if (target_y < 0):
						target_y += width
				elif direction == GAME_MOVE_E:
					target_y += 1
					if (target_y >= width):
						target_y -= width
				else:
					return False


				target_tile = self.planet.tiles[target_x * width + target_y]
				if target_tile.is_slope:
					if target_tile.elevation[0] == self.elevation:
						self.elevation = target_tile.elevation[1]
					elif target_tile.elevation[1] == self.elevation:
						self.elevation = target_tile.elevation[0]
					else:
						break
				else:
					if target_tile.elevation != self.elevation:
						break
					else:
						pass

				self.x = target_x
				self.y = target_y
				if target_tile.is_shaded():
					self.battery -= 1
				if target_tile.explored == False:
					target_tile.explored = True
					self.explored_num += 1
			return True


			pass

	def wait(self, cycles):
		"""
		The rover will wait for the specified cycles
		"""
		width = self.planet.get_width()
		current_tile = self.planet.tiles[self.x * width + self.y]

		if current_tile.is_shaded():
			pass
		else:
			self.battery += cycles
			if self.battery > 100:
				self.battery = 100
		pass



