import requests
import json
#TODO: This needs caching.  Badly.
class BuildingList:
	buildings={}
	allbuildings=[]
	def __init__(self,key="487096119dcbbbbca9a399417e594713"):
		r=requests.get("https://api.uwaterloo.ca/v2/buildings/list.json?key="+key)
		if str(r.status_code) != "200": #
			raise uWatelooApiError
		else:
			for building in json.loads(r.text)["data"]:
				self.buildings[building["building_code"]]=building["building_name"]
				self.allbuildings.append(building["building_name"])
	def __getitem__(self,key):
		return self.buildings[key]

	def __iter__(self):
		return self.allbuildings.__iter__()