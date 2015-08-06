from db import Database
import web
import json
"""
Implements /getnextclass from API
"""
class GetNextClassServlet:
	def GET(self):
		dbase=Database()

		user_data = web.input()
		if not dbase.verify_user(user_data.userid, user_data.token):
			return "Please authenticate when using the API"
		cls=dbase.getNextClass(user_data.userid)
		cls.timestamp=cls.timestamp.strftime("%H:%M %m/%d/%Y") # JSON friendly date formats.
		cls.timeend=cls.timeend.strftime("%H:%M %m/%d/%Y")
		dclass={"id":cls.id,"class_name":cls.class_name,"section":cls.section,"timestamp":cls.timestamp,"timeend":cls.timeend,"instructor":cls.instructor,"type":cls.type,"where":cls.where}
		json.dumps(dclass)