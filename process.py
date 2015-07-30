from calc import pathFinder
from calc import edgeBuilder
from parsers import osm
from viewer import NodeCollection,Node

nC=NodeCollection()
nC.load()
nC.dedupe()
nC.save()
pF=pathFinder(nC)
pF.build()
