from db import Database
import redis
import json
import web
"""
Implements GetClosestNode API endpoint.
"""

class ClosestNodeServlet:
	def GET(self):
		dbase=Database()
		inp=web.input()
		nd=dbase.getClosestNode(inp.lat,inp.lon)
		return '{"id":"'+str(nd.id)+'","lat":"'+str(nd.lat)+'","lon":"'+str(nd.lon)+'","name":"'+str(nd.name)+'"}'
