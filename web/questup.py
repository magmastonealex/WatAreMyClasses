import web
from jinja2 import Environment, PackageLoader
from parsers import Quest
from db import Database
from services import Auth

"""
Deals with quest/onboarding. Walks user through adding new schedule.
When completed correctly, redirects to /map.

Note the POST/GET syntax examples.

Source: quest.html
Current Mapping: /onboard
"""
class QuestUploadServlet:
	def GET(self):
		env = Environment(loader=PackageLoader('html', ''))
		template = env.get_template('quest.html')
		return template.render()
	def POST(self):
		dbase=Database()
		ath=Auth(dbase)
		if not ath.checkAuth():
			raise web.seeother('/')
		inp=web.input(quest="")
		if inp["quest"] != "":
			q=Quest(dbase)
			q.getSched(inp["quest"],ath.getUserid())
			dbase.user_setold(ath.getUserid())
			raise web.seeother('/map')
		else:
			return "Please go back and actually submit something."
		# redirect(CASLoginURL)