import json
from db import Database
"""
Quest schedule parser. Meant to be run soley on web-tier

Takes the DB in it's init.

getSched(inp,uid) takes the raw Quest text dump from a text field (textarea! Needs the linebreaks!) and puts the schedule in the DB.
Attaches to the userID provided. DOES NOT CLEAR OLD SCHEDULE YET!
Probably should re-factor to change the name.


"""
class Quest:
	def __init__(self,db):
		self.db=db;
	def getSched(self,inp,uid):
		schedalls=json.loads(inp)
		for item in schedalls:
			self.db.run_sql("INSERT INTO timetable (uname,building,time,time_end,cls,sec,tpe,prof) VALUES(%s,%s,to_timestamp(%s, 'yyyy-mm-dd hh24:mi'),to_timestamp(%s, 'yyyy-mm-dd hh24:mi'),%s,%s,%s,%s)",(uid,item["building"],item["time"],item["time_end"],item["cls"],item["sec"],item["tpe"],item["prof"].replace("'","").replace('"',"")))
				