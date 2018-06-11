
class Planet:
	def __init__(self, name, width, height, tiles):
		"""
		Initialise the planet object
		"""
		self.name = name
		self.width = width
		self.height = height
		self.tiles = tiles
		self.tile_num = width * height


	def get_width(self):
		return self.width

	def get_height(self):
		return self.height







