import unittest
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) # black magic because imports from parents are strange.

from parsers import osm

class fakeNodeCollection:
	vertices={}
	def addNode(self,ID,*args,**kwargs):
		try:
			self.vertices[ID]={	"id":ID,"x":args[0],"y":args[1],"name":kwargs["name"]}
		except:
			self.vertices[ID]={	"id":ID,"x":args[0],"y":args[1]}
	def __getitem__(self,key):
		return self.vertices[key]

class TestOSM(unittest.TestCase):

	def test_collect_nodes(self):
		o=osm("tests/osm_getnodes_test.xml",None)
		o.open()
		o.collectNodes()
		self.assertEqual(o.tempNodes, {'277308883': [43.4666273, -80.539957], '277307823': [43.470883, -80.5381226], '277307822': [43.464492, -80.5415116], '114158644': [43.4709026, -80.5379042]})
	def test_get_building(self):
		fnc=fakeNodeCollection()
		o=osm("tests/osm_getbuilding_test.xml",fnc)
		o.open()
		o.collectNodes()
		o.getBuilding("Engineering 3")
		self.assertEqual(fnc.vertices, {'b-Engineering 3': {'y': -80.540763028543751, 'x': 43.471711768964454, 'id': 'b-Engineering 3', 'name': 'Engineering 3'}})

if __name__ == '__main__':
	unittest.main()