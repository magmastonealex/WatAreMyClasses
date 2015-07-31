import unittest
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) # black magic because imports from parents are strange.

from calc import edgeBuilder
from LatLon import LatLon
from viewer import Node

class fakeNodeCollection:
	vertices={}
	edges=[]
	def __init__(self):
		self.vertices["test1"]=Node("test1",43.726797, -79.782870,latlong=LatLon(43.726797, -79.782870))
		self.vertices["test2"]=Node("test2",43.726782, -79.782835,latlong=LatLon(43.726782, -79.782835))
		self.vertices["test3"]=Node("test3",43.726761, -79.782808,latlong=LatLon(43.726761, -79.782808))
	def __getitem__(self,key):
		return self.vertices[key]
	def addEdge(self,id1,id2,dist):
		self.edges.append([id1,id2,dist])

class TestOSM(unittest.TestCase):

	def test_edge_builder(self):
		#this really only tests if adds the right number of edges, not that the edges are necessarily correct
		fnc=fakeNodeCollection()
		eB=edgeBuilder(fnc)
		eB.build()
		print fnc.edges
		self.assertEqual(len(fnc.edges), len([['test1', 'test3', 6], ['test3', 'test1', 6], ['test1', 'test2', 3], ['test2', 'test1', 3], ['test3', 'test2', 3], ['test2', 'test3', 3]]))


if __name__ == '__main__':
	unittest.main()