from db import Database
import redis
import json

"""
Implements BuildingList API endpoint.
Makes use of caching.
"""

class BuildingListServlet:
	def GET(self):
		r=redis.Redis()
		web.header("Content-Type","application/json")
		ccheck=r.get("allblds")
		if  ccheck != None:
			print "cachehit"
			return ccheck
		print "cachemiss"
		x=r.keys("building:*")
		blds={}	
		for k in x:
			blds[k]=r.get(k)
		ret=json.dumps(blds)
		r.set("allblds",ret)

		return ret