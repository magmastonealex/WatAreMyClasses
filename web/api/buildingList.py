from db import Database
import redis
import json
import web
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
		allblds=[]
		for k in x:
			blds={}
			blds["id"]=k.split("building:")[1]
			blds["name"]=r.get(k)
			allblds.append(blds)
		ret=json.dumps(allblds)
		r.set("allblds",ret)

		return ret
