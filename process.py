from calc import pathFinder
from calc import edgeBuilder
from parsers import osm
from viewer import NodeCollection,Node

nC=NodeCollection()
nC.load("out.nodecollection")
nds=open("nodes.sql","w")
ndsR=open("nodes.redis","w")
for nodeID,node in nC.vertices.items():
	nds.write("INSERT INTO nodes (id,name,lat,long) VALUES ('"+nodeID+"','"+node.name+"',"+str(node.x)+","+str(node.y)+");\n")
	ndsR.write("SET 'nodes:"+nodeID+"' '"+str(node.x)+","+str(node.y)+","+node.name+"'\n")
nds.close()
ndsR.close()
#pF=pathFinder(nC)
#pF.build()
