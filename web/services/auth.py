import web

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
			