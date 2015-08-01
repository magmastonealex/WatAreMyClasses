import web
from caslib import CASClient
class CASpyServlet:
	def GET(self):
		cas_client = CASClient("https://cas.uwaterloo.ca/cas","http://localhost/test?sendback=/test")
		getvars=web.input()
		ticket_from_cas = getvars['ticket']
		print cas_client._service_validate_url(ticket_from_cas)
		cas_response = cas_client.cas_serviceValidate(ticket_from_cas)
		#cas_response object
		print cas_response
		(truth, user) = (cas_response.success, cas_response.user)
		if (truth):
			return "good2go"
		else:
			return "ded"
		# redirect(CASLoginURL)