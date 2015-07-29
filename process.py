from calc import pathFinder
from calc import edgeBuilder
from parsers import osm


ma=osm("mapdata.xml")
ma.runAll()

edges=ma.edges
paths=ma.paths
ngraph=ma.ngraph
nodes=ma.nodes

eb=edgeBuilder(edges,ngraph,nodes)
eb.makeDataValid()
edges=eb.edges
ngraph=eb.ngraph

pF=pathFinder(edges)
pF.makeDataValid()
