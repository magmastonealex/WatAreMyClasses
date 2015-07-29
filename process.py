from calc import pathFinder
from calc import edgeBuilder
from parsers import osm
from viewer import NodeCollection,Node

nC=NodeCollection()
#nC.load()


ma=osm("mapdata2.xml",nC)
ma.runAll()
nC.save()

eB=edgeBuilder(nC)
eB.build()
nC.save()

nC.dedupe()
pF=pathFinder(nC)
pF.build()
