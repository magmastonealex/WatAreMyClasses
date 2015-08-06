#! /bin/python
import os
os.chdir(os.path.dirname(os.path.realpath(__file__))) # then we can use abs path.
import web
from index import IndexServlet
from caspy import CASpyServlet
from questup import QuestUploadServlet

from landing import LandingServlet

from api import *

"""
Main class. Code doesn't go here, but path definitions do.

Syntax: '/url','ClassName'

Make sure to import your class above!

Usual format is to have url handlers stay in the root module.
"""
urls = (
	'/','LandingServlet',
	'/map', 'IndexServlet',
	'/login', 'CASpyServlet',
	'/onboard', 'QuestUploadServlet',
	'/getpath',  'PathAPIServlet',
	'/buildinglist','BuildingListServlet',
	'/getclosestnode','ClosestNodeServlet',
	'/getschedule','GetScheduleServlet',
	'/getnextclass','GetNextClassServlet'
)


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()