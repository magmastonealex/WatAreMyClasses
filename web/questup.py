import web
from jinja2 import Environment, PackageLoader
from parsers import Quest
from db import Database

class QuestUploadServlet:
	def GET(self):
		env = Environment(loader=PackageLoader('html', ''))
		template = env.get_template('quest.html')
		return template.render(vertices=xs,path=pth)
	def POST(self):
		dbase=Database()
		inp=web.input(quest="badquesty")
		if inp["quest"] != "badquesty":
			q=Quest(dbase)
			q.getSched(inp["quest"])
			return "Thanks!"
		else:
			return "Please actually submit something."
		# redirect(CASLoginURL)