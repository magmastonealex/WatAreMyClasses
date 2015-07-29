from calc import pathFinder
from calc import edgeBuilder
from parsers import osm
from viewer import NodeCollection,Node

nC=NodeCollection()
nC.load()

pF=pathFinder(nC)
pF.build()

#ma=osm("mapdata2.xml",nC)
#ma.runAll()
#nC.save()
#print nC.edges
#print nC.vertices

#eB=edgeBuilder(nC)
#eB.build()
#nC.save()

#pF=pathFinder(edges)
#pF.makeDataValid()
