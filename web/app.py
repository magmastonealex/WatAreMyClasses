#! /bin/python

import web
from index import IndexServlet

urls = (
	'/', 'IndexServlet'
)


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()