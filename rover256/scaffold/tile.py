
class Tile:
		
	def __init__(self,is_slope,shaded,elevation):
		"""
		Initialises the terrain tile and attributes
		"""
		self.is_slope = is_slope
		self.shaded = shaded
		self.elevation = elevation
		self.occupant = None
		self.explored = False

	def elevation(self):
		"""
		Returns an integer value of the elevation number 
		of the terrain object
		"""
		return self.elevation
	
	def is_shaded(self):
		"""
		Returns True if the terrain tile is shaded, otherwise False
		"""
		return self.shaded
	
	def set_occupant(self, obj):
		"""
		Sets the occupant on the terrain tile
		"""
		self.occupant = obj
		self.explored = True
		obj.elevation = self.elevation
		obj.shaded = self.shaded
	
	def get_occupant(self):
		"""
		Gets the entity on the terrain tile
		If nothing is on this tile, it should return None
		"""
		return self.occupant
	
	
