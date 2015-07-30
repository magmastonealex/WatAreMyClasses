import requests
import json

class BuildingList:
	buildings={}
	allbuildings=[]
	def __init__(self,key):
		r=requests.get("https://api.uwaterloo.ca/v2/buildings/list.json?key="+key)
		if str(r.status_code) != "200": #
			raise uWatelooApiError
		else:
			for building in json.loads(r.text)["data"]:
				buildings[building["building_code"]]=building["building_name"]
				allbuildings.append(building["building_name"])
	def __getitem__(self,key):
		return buildings[key]
