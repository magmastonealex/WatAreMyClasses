from jinja2 import Environment, PackageLoader
from viewer import NodeCollection,Node
from services import Paths
import web


"""
beep,boop, please ignore.
"""

pt = Paths()
env = Environment(loader=PackageLoader('html', ''))
template = env.get_template('maptest.html')
nC=NodeCollection()
nC.load()

xs=[]

pth=[]

for el in pt.getPath("2016012246","b-Engineering 3"):
	pth.append([nC[el].x,nC[el].y])
	xs.append(nC[el])


print template.render(vertices=xs,path=pth)