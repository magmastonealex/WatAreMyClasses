from calc import pathFinder_Threaded
from calc import edgeBuilder
from parsers import osm
from parsers import BuildingList
from viewer import NodeCollection,Node

"""
This script does all of the cache-prep work for the web-tier to speed up requests.
Run it, and look at docs/Data Import.md to see how to deploy.
"""


#113 496
# 18 468
x=BuildingList()

bldR=open("buildings.redis","w")
for code,building in x.buildings.items():
	bldR.write("SET 'building:"+code+"' '"+building.replace("'","")+"'\n")
bldR.close()


nC=NodeCollection()
nC.load("out.nodecollection")
OSM=osm("mapdata-whole.xml",nC) #Whole campus. Letsdothisthing.

OSM.runAll(x.buildings)
eB=edgeBuilder(nC)
eB.build()
nC.dedupe()
nC.save("out.nodecollection")
nds=open("nodes.sql","w")
ndsR=open("nodes.redis","w")
for nodeID,node in nC.vertices.items():
	nds.write("INSERT INTO nodes (id,name,lat,long) VALUES ('"+nodeID+"','"+node.name+"',"+str(node.x)+","+str(node.y)+");\n")#
	ndsR.write("SET 'nodes:"+nodeID+"' '"+str(node.x)+","+str(node.y)+","+node.name+"'\n")
nds.close()
ndsR.close()


#Only run if absolutely needed... Takes a very long time
pF=pathFinder_Threaded(nC)
pF.build()
