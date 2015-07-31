"""
WebNode is different from a Node, but serves the same purpose.

"""
class WebNode:
	def __init__(self,ID,lat,lon,name):
		self.id=ID
		self.lat=lat
		self.lon=lon
		self.x=lat #Preserve compatability.
		self.y=lon
		self.name=name