import psycopg2
import redis
from model import WaterlooClassTime,WebNode
"""
Sole object for database interaction in web-tier. No need to include viewer/other class definition files.
Methods:

getNode(nodeid) # Gives node in dictinary format with lat,long,name.
getClosest_node(ulat,ulong) # given user lat and long, returns the closest node.
getNextClass(userid) # for a given user, get their next class.

"""
class Database:
	def __init__(self):
		self.red = redis.Redis()
		self.dbconn=psycopg2.connect("dbname='postgres' host='localhost' user='postgres' password='ourpasswordissosecure'")
	def getNode(self,nodeid):
		x=self.red.get("nodes:"+nodeid).split(",")
		return WebNode(nodeid,x[0],x[1],x[2]) # ID, lat, long, name
	def getClosestNode(self,ulat,ulong):
		cur = self.dbconn.cursor()
		cur.execute("SELECT nodes.id, nodes.name,nodes.lat, nodes.long, earth_distance(ll_to_earth("+str(ulat)+","+str(ulong)+" ), ll_to_earth(nodes.lat, nodes.long)) as distance_from_current_location FROM nodes ORDER BY distance_from_current_location ASC LIMIT 1;")
		rows = cur.fetchall()
		closestnode=rows[0]
		return WebNode(closestnode[0],closestnode[2],closestnode[3],closestnode[1]) # ID, lat, long, name
	def getNextClass(self,userid):
		cur = self.dbconn.cursor()
		cur.execute("SELECT timetable.id,timetable.cls,timetable.tpe,timetable.sec,timetable.prof,timetable.building,timetable.time,timetable.time_end FROM timetable WHERE time > now() ORDER BY time ASC LIMIT 1;")
		rows = cur.fetchall()
		nextclass=rows[0]
		return WaterlooClassTime(nextclass[0],nextclass[1],nextclass[3],nextclass[6],nextclass[7],nextclass[4],nextclass[2],nextclass[5])
	def run_sql(self,sql,params):
		cur = self.dbconn.cursor()
		try:
			cur.execute(sql,params)
			self.dbconn.commit()
		except psycopg2.Error as e:
			print "ERROR! "+e.pgerror
#								#(ID,class_name,section,timestamp,timeend,instructor,type,building-room