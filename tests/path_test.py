import unittest
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) # black magic because imports from parents are strange.

from calc import pathFinder

class fakeNodeCollection:
	edges=[]

class TestPath(unittest.TestCase):

	def test_basics_dist(self):
		fnc=fakeNodeCollection()
		fnc.edges=[("1040","1090",4),("1090","4273",10)]
		pF=pathFinder(fnc)
		pF.build(test=True)
		self.assertEqual(pF.dist, {'4273': {'4273': 0, '1040': 14, '1090': 10}, '1040': {'4273': 14, '1040': 0, '1090': 4}, '1090': {'4273': 10, '1040': 4, '1090': 0}})
	def test_basics_nex(self):
		fnc=fakeNodeCollection()
		fnc.edges=[("1040","1090",4),("1090","4273",10)]
		pF=pathFinder(fnc)
		pF.build(test=True)
		self.assertEqual(pF.nex, {'4273': {'1040': '1090', '1090': '1090'}, '1040': {'4273': '1090', '1090': '1090'}, '1090': {'4273': '4273', '1040': '1040'}})
	def test_complex_dist(self):
		fnc=fakeNodeCollection()
		fnc.edges=[("1040","1090",40),("1040","4092",30),("4092","2034",20),("1090","3024",50)]
		pF=pathFinder(fnc)
		pF.build(test=True)
		self.assertEqual(pF.dist, {'4092': {'4092': 0, '3024': 120, '1040': 30, '1090': 70, '2034': 20}, '3024': {'4092': 120, '3024': 0, '1040': 90, '1090': 50, '2034': 140}, '1040': {'4092': 30, '2034': 50, '1090': 40, '3024': 90, '1040': 0}, '1090': {'1090': 0, '4092': 70, '1040': 40, '3024': 50, '2034': 90}, '2034': {'4092': 20, '1040': 50, '1090': 90, '3024': 140, '2034': 0}})
	def test_complex_nex(self):
		fnc=fakeNodeCollection()
		fnc.edges=[("1040","1090",40),("1040","4092",30),("4092","2034",20),("1090","3024",50)]
		pF=pathFinder(fnc)
		pF.build(test=True)
		self.assertEqual(pF.nex, {'4092': {'3024': '1040', '1040': '1040', '1090': '1040', '2034': '2034'}, '3024': {'4092': '1090', '1040': '1090', '1090': '1090', '2034': '1090'}, '1040': {'4092': '4092', '2034': '4092', '1090': '1090', '3024': '1090'}, '1090': {'4092': '1040', '1040': '1040', '3024': '3024', '2034': '1040'}, '2034': {'4092': '4092', '1040': '4092', '1090': '4092', '3024': '4092'}})
	def test_complex_path(self):
		fnc=fakeNodeCollection()
		fnc.edges=[("1040","1090",40),("1040","4092",30),("4092","2034",20),("1090","3024",50)]
		pF=pathFinder(fnc)
		pF.build(test=True)
		self.assertEqual(pF.findPath("2034","3024"), ["2034","4092","1040","1090","3024"])


if __name__ == '__main__':
	unittest.main()