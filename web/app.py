#! /bin/python
import os
os.chdir(os.path.dirname(os.path.realpath(__file__))) # then we can use abs path.
import web
from index import IndexServlet
from caspy import CASpyServlet
from questup import QuestUploadServlet
from path_api import PathAPIServlet

urls = (
	'/', 'IndexServlet',
	'/login', 'CASpyServlet',
	'/onboard', 'QuestUploadServlet',
	'/getpath',  'PathAPIServlet'
)


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()