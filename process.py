from calc import pathFinder
from calc import edgeBuilder
from parsers import osm
from parsers import BuildingList
from viewer import NodeCollection,Node

"""
This script does all of the cache-prep work for the web-tier to speed up requests.
Run it, and look at docs/Data Import.md to see how to deploy.
"""



x=BuildingList()

bldR=open("buildings.redis","w")
for code,building in x.buildings.items():
	bldR.write("SET 'building:"+code+"' '"+building.replace("'","")+"'\n")
bldR.close()

exit()

nC=NodeCollection()
OSM=osm("mapdata2.xml",nC)
OSM.runAll()
eB=edgeBuilder(nC)
eB.build()
nC.dedupe()
nC.save("out.nodecollection")
nds=open("nodes.sql","w")
ndsR=open("nodes.redis","w")
for nodeID,node in nC.vertices.items():
	nds.write("INSERT INTO nodes (id,name,lat,long) VALUES ('"+nodeID+"','"+node.name+"',"+str(node.x)+","+str(node.y)+");\n")
	ndsR.write("SET 'nodes:"+nodeID+"' '"+str(node.x)+","+str(node.y)+","+node.name+"'\n")
nds.close()
ndsR.close()
#Only run if absolutely needed... Takes a very long time
#pF=pathFinder(nC)
#pF.build()
