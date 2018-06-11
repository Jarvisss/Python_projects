from scaffold.planet import Planet
from scaffold.rover import Rover
from scaffold.tile import Tile

TAG_PLANET = "[planet]"
PLANET_ATTRIBUTE_NAME = "name"
PLANET_ATTRIBUTE_WIDTH = "width"
PLANET_ATTRIBUTE_HEIGHT = "height"
PLANET_ATTRIBUTE_ROVER_POSITION = "rover"

TAG_TILES = "[tiles]"
TILE_TYPE_PLAIN = "plains"
TILE_TYPE_SHADE = "shaded"


def load_level(file_name):
	"""
	Loads the level and returns an object of your choosing
	"""

	tile_map = []
	rover = None

	name = None
	width = 0
	height = 0
	num_tiles = 0
	rover_x = 0
	rover_y = 0
	with open(file_name,'r') as f:
		### remove empty lines
		line = f.readline().strip('\n')
		if line == '':
			while True:
				line = f.readline().strip('\n')
				if line != '':
					break

		### first line should be "[planet]"
		if line == TAG_PLANET:
			### read name
			name_line = f.readline()
			name = get_one_attribute_value(name_line, PLANET_ATTRIBUTE_NAME)
			if name == None:
				return None

			### read width
			width_line = f.readline()
			try:
				width = int(get_one_attribute_value(width_line, PLANET_ATTRIBUTE_WIDTH))
			except ValueError:
				return None

			### read height
			height_line = f.readline()
			#### check if integer
			try:
				height = int(get_one_attribute_value(height_line, PLANET_ATTRIBUTE_HEIGHT))
			except ValueError:
				return None


			### read rover coordinate
			rover_line = f.readline()
			rover_coordinate = get_two_attribute_values(rover_line, PLANET_ATTRIBUTE_ROVER_POSITION)
			#### check para num
			if len(rover_coordinate) != 2:
				return None
			try:
				rover_x = int(rover_coordinate[0])
				rover_y = int(rover_coordinate[1])
			except ValueError:
				return None

			if rover_x >=width or rover_y >=height\
					or rover_x < 0 or rover_y < 0:
				return None


			### remove empty lines
			line = f.readline().strip('\n')
			if line == '':
				while True:
					line = f.readline().strip('\n')
					if line != '':
						break
					else:
						continue

			### should at least an empty line between [planet] and [tiles]
			else:
				return None
			num_tiles = width * height
			if line == TAG_TILES:
				for _ in range(num_tiles):
					### read name
					tiles_line = f.readline()
					tile = get_tile(tile_str=tiles_line)
					if tile == None:
						### error reading tile file
						return None
					else:
						tile_map.append(tile)


				planet = Planet(name=name, width=width, height=height, tiles=tile_map)
				rover = Rover(x=rover_x, y=rover_y, planet=planet)
				return rover
		### Wrong Structure
		else:
			return None

def get_one_attribute_value(line_str, attr_name):
	"""
	:param line_str: one line in "attr,value" format
	:param attr_name: "attr"
	:return: value
	"""
	line_str = line_str.strip('\n')
	line_array = line_str.split(',')
	if len(line_array) != 2:
		return None
	elif line_array[0]!=attr_name:
		return None
	else:
		return line_array[1]

def get_two_attribute_values(line_str, attr_name):
	"""
	:param line_str: one line in "attr,value" format
	:param attr_name: "attr"
	:return: [value1, value2]
	"""
	line_str = line_str.strip('\n')
	line_array = line_str.split(',')
	if len(line_array) != 3:
		return None
	elif line_array[0]!=attr_name:
		return None
	else:
		return [line_array[1], line_array[2]]

def get_tile(tile_str):
	"""
	:param tile_str: one line in "Terrain,[values...]" format
	:return:Terrain, [values...]
	"""
	tile_str = tile_str.strip('\n')
	tile_array = tile_str.split(',')
	tile_arg_num = len(tile_array)
	### 2 or 3 arguments should be accepted
	if tile_arg_num > 3 or tile_arg_num <2:
		return None
	### only two types should be accepted
	elif tile_array[0] != TILE_TYPE_PLAIN and tile_array[0] != TILE_TYPE_SHADE:
		return None

	elif tile_arg_num == 3:
		try:
			high = int(tile_array[1])
			low = int(tile_array[2])
		except ValueError:
			return None

		### only a diff of 1
		if (high-low) != 1:
			return None
		else:
			if tile_array[0] == TILE_TYPE_PLAIN:
				return Tile(is_slope=True,shaded=False,elevation=[high,low])
			elif tile_array[0] == TILE_TYPE_SHADE:
				return Tile(is_slope=True, shaded=True, elevation=[high, low])

	elif tile_arg_num == 2:
		try:
			elevation = int(tile_array[1])
		except ValueError:
			return None

		if tile_array[0] == TILE_TYPE_PLAIN:
			return Tile(is_slope=False, shaded=False, elevation=elevation)
		elif tile_array[0] == TILE_TYPE_SHADE:
			return Tile(is_slope=False, shaded=True, elevation=elevation)

