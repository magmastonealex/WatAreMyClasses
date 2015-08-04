import psycopg2
import redis
from model import WaterlooClassTime,WebNode
"""
Sole object for database interaction in web-tier. No need to include viewer/other class definition files.
Methods:

getNode(nodeid) # Gives node in dictinary format with lat,long,name.
getClosest_node(ulat,ulong) # given user lat and long, returns the closest node.
getNextClass(userid) # for a given user, get their next class.
getDayClasses(userid) # for a given user, get all the classes of the day, by time.
get_building_name(code) # Gives the full name of a building given it's 3-5 letter code. (RCH,SLC,MC,M3)

run_sql(sql,params) # runs a query against Postgres. Takes a tuple of params. 
					# use: db.run_sql("SELECT * from timetable where uname=%s",("me@magmastone.net",))
					# Never use quotes!
get_redis(key) # direct Redis getter
set_redis(key,data) # direct Redis setter.


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
	def getDayClasses(self,userid):
		cur = self.dbconn.cursor()
		#cur.execute("SELECT timetable.id,timetable.cls,timetable.tpe,timetable.sec,timetable.prof,timetable.building,timetable.time,timetable.time_end FROM timetable WHERE time > TIMESTAMP 'today' AND time < TIMESTAMP 'tomorrow' ORDER BY time ASC")
		cur.execute("SELECT timetable.id,timetable.cls,timetable.tpe,timetable.sec,timetable.prof,timetable.building,timetable.time,timetable.time_end FROM timetable WHERE time > to_timestamp('15/09/2015','dd/mm/yyyy') AND time < to_timestamp('16/09/2015','dd/mm/yyyy') ORDER BY time ASC;")
		classes=[]
		rows = cur.fetchall()
		for nextclass in rows:
			classes.append(WaterlooClassTime(nextclass[0],nextclass[1],nextclass[3],nextclass[6],nextclass[7],nextclass[4],nextclass[2],nextclass[5]));
		return classes
	def run_sql(self,sql,params):
		cur = self.dbconn.cursor()
		try:
			cur.execute(sql,params)
			self.dbconn.commit()
		except psycopg2.Error as e:
			print "ERROR! "+e.pgerror
	def get_redis(self,key):
		return self.red.get(key)

	def set_redis(self,key,data):
		return self.red.set(key,data)

	def get_building_name(self,code):
		return self.get_redis("building:"+code) # keep it portable!