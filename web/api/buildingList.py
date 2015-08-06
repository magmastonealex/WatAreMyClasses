from db import Database
import redis
import json

"""
Implements BuildingList API endpoint.
Makes use of caching.
"""

class BuildingList:
	def GET():
		r=redis.Redis()
		ccheck=r.get("allblds")
		if  ccheck != None:
			return ccheck
		x=r.keys("building:*")
		blds={}	
		for k in x:
			blds[k]=x
		ret=json.dumps(blds)
		r.set("allblds",ret)
		return ret