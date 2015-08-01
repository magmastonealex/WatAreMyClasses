#! /bin/python
import os
os.chdir(os.path.dirname(os.path.realpath(__file__))) # then we can use abs path.
import web
from index import IndexServlet
from caspy import CASpyServlet
from questup import QuestUploadServlet

urls = (
	'/', 'IndexServlet',
	'/test', 'CASpyServlet'
	'/questup', 'QuestUploadServlet'
)


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()