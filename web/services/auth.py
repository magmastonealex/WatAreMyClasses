import web

"""
Basic authentication class.
Usage:

x = Auth(database) - initialize with a Database object. Side note: Python needs singleton support.

x.checkAuth() - Does all the work required to test if a user is authenticated already.
!!Does NOT redirect the user back to the login page!!

x.getUserid() - Convienience to return the current UserID.
x.getUserToken() - Convienience to return current user's token
"""

class Auth:
	def __init__(self,dbase):
		self.db=dbase
	def checkAuth(self):
		token=web.cookies().get("token")
		user=web.cookies().get("user")
		if self.db.verify_user(user,token):
			return True
		else:
			print "please login"
			return False
	def getUserid(self):
		return web.cookies().get("user")
	def getUserToken(self):
		return web.cookies().get("token")