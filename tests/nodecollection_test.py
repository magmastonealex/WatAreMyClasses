import unittest
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) # black magic because imports from parents are strange.

import random, LatLon
from viewer import Node, NodeCollection

class NodeCollectionTestMethods(unittest.TestCase):
	def setUp(self):
		self.source=NodeCollection()
		for i in range(50):
			self.source.addNode(i,random.randint(20,800-20),random.randint(20,600-20))
		for i in range(3):
			self.source.addEdge(random.randint(0,49),random.randint(0,49),1)

	def tearDown(self):
		try:
			os.remove("tests/nodecollection_temp.txt")
		except:	#file not found
			pass

	def testEdgeLengthSymmetry(self):
		"""checks that if an edge exists from A->B, a path of equal length exists from B->A"""
		for ID,vertex in self.source.vertices.iteritems():
			for otherVertex in vertex.adjacent:
				self.source[otherVertex].adjacent[ID]
				self.assertEqual(vertex.adjacent[otherVertex], self.source[otherVertex].adjacent[ID])

	def testSavingPreservesN(self):
		"""Checks """
		self.source.save("tests/nodecollection_temp.txt")

		copy=NodeCollection()
		copy.load("tests/nodecollection_temp.txt")

		self.assertEqual(len(self.source.vertices),len(copy.vertices))
		self.assertEqual(len(self.source.edges),len(copy.edges))

		for node in copy.vertices:
			for otherNode in copy[node].adjacent.keys():
				self.assertTrue(otherNode in self.source[node].adjacent)

	def testSavingPreservesStringForm(self):
		"""Tests that the save file of a copy is identical to the save file that it was loaded from."""
		self.source.save("tests/nodecollection_temp.txt")
		copy=NodeCollection()
		copy.load("tests/nodecollection_temp.txt")
		self.assertEqual(self.source.getSaveString(), copy.getSaveString())

	def testSavingPreservesSingleNode(self):
		self.source=NodeCollection()
		self.source.addNode(1,2,3,name="asdfasdn")
		self.source.save("tests/nodecollection_temp.txt")
		self.source.load("tests/nodecollection_temp.txt")

		self.assertEqual(self.source.vertices["1"].id,"1")
		self.assertEqual(self.source.vertices["1"].x,2.)
		self.assertEqual(self.source.vertices["1"].y,3.)
		self.assertEqual(self.source.vertices["1"].adjacent,{})

if __name__ == "__main__":
	unittest.main()
