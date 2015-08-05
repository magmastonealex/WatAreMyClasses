from jinja2 import Environment, PackageLoader
from db import Database
from model import WaterlooClassTime,WebNode
from services import Paths
import web
import datetime
from services import Auth

"""
Initial homepage servlet.

Source: landing.html
Current Mapping: /
"""

class LandingServlet:
	def GET(self):
		dbase=Database()
		ath=Auth(dbase)
		if ath.checkAuth():
			raise web.seeother('/map')
		tkn,new=dbase.user_exists(ath.getUserid())
		if new == True:
			raise web.seeother("/onboard")
		env = Environment(loader=PackageLoader('html', ''))
		template = env.get_template('landing.html')
		
		return template.render()