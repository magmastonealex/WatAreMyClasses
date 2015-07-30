#not a real unit test, but a show of how pathfinding could work.
from calc import pathFinder

pF=pathFinder(None)
pF.load()

print pF.findPath("1923753475","2016012246") # any two node ids!
print pF.dist["1923753475"]["2016012246"]