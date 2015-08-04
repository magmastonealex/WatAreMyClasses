import web
from caslib import CASClient
from db import Database
class CASpyServlet:
	def GET(self):
		cas_client = CASClient("https://cas.uwaterloo.ca/","http://ssvps.magmastone.net/login")
		getvars=web.input(ticket="none")
		ticket_from_cas = getvars['ticket']
		if ticket_from_cas=="none":
			raise web.seeother('https://cas.uwaterloo.ca/cas/login?service=http://ssvps.magmastone.net/login')
		print cas_client._service_validate_url(ticket_from_cas)
		cas_response = cas_client.cas_serviceValidate(ticket_from_cas)
		#cas_response object
		print cas_response
		(truth, user) = (cas_response.success, cas_response.user)
		if (truth):
			db=Database()
			token,new=db.user_exists(user)
			if token==False:
				token=db.user_create(user)
				new=True
			web.setcookie("token",token)
			web.setcookie("user",user)
			web.setcookie("new",new)
			raise web.seeother('/')
		else:
			return "Login failed!"
		# redirect(CASLoginURL)