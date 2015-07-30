import pygame, random

from viewer import NodeCollection,Node
from calc import pathFinder

"""Draws vertices and edges to the screen. Currently randomly generates vertices and edges.
Hold left mouse button down and drag to pan.
Scroll mouse wheel to zoom in and out."""

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Viewer:
	"""Dedicated viewing class for NodeCollections."""
	def __init__(self,nodeCollection,width=800,height=600):
		self.nodeCollection=nodeCollection
		self.width=width
		self.height=height
		
		self.pathFind=pathFinder(self.nodeCollection)
		self.pathFind.load()

		self.pathFound=self.pathFind.findPath("2016012246","b-Engineering 3")
		#pick an initial camerax, cameray, zoom factor such that you can see the entire screen
		maxX=max([node.x for node in self.nodeCollection.vertices.values()])
		minX=min([node.x for node in self.nodeCollection.vertices.values()])
		maxY=max([node.y for node in self.nodeCollection.vertices.values()])
		minY=min([node.y for node in self.nodeCollection.vertices.values()])
		#self.camerax=int((maxX+minX)/2)
		#self.cameray=int((maxY+minY)/2)
		#self.zoom=min((maxX-minX)/2, (maxY-minY)/2)
		self.camerax=43.4723642752
		self.cameray=-80.5403881748
		self.zoom=83372.7046559

	def transform(self, x, y):
		return int((x-self.camerax)*self.zoom + self.width/2), int((y-self.cameray)*self.zoom + self.height/2)

	def run(self):
		"""Until I figure out some clever way of parallelizing this, Viewer.run() basically halts your program execution to show you a viewer, until you exit the window."""
		pygame.init()
		screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("map data visualizer")

		run=True
		clock = pygame.time.Clock()
		update=True

		while run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				elif event.type == pygame.MOUSEMOTION:
					if event.buttons[0]:
						self.camerax-=event.rel[0]/self.zoom
						self.cameray-=event.rel[1]/self.zoom
						print str(self.camerax)+","+str(self.cameray)
						update=True
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button==4:	#zoom in
						self.zoom*=1.1
						update=True
						print self.zoom
					elif event.button==5:
						self.zoom/=1.1
						update=True
						print self.zoom

			if update:
				screen.fill(BLACK)
				for edge in self.nodeCollection.edges:
					pygame.draw.aalines(screen, RED, True, [
							self.transform(self.nodeCollection[edge[0]].x, self.nodeCollection[edge[0]].y),
							self.transform(self.nodeCollection[edge[1]].x, self.nodeCollection[edge[1]].y)])

				for point in self.nodeCollection.vertices.values():
					if point.name != "":
						pygame.draw.circle(screen, BLUE, self.transform(point.x, point.y), 6)
					else:
						pygame.draw.circle(screen, WHITE, self.transform(point.x, point.y), 2)
				
				lns=[]
				for point in self.pathFound:
					lns.append(self.transform(self.nodeCollection[point].x, self.nodeCollection[point].y))
				print lns
				pygame.draw.lines(screen,GREEN,False,lns,10)
				update=False

			
			clock.tick(30)
			pygame.display.flip()
		

		pygame.quit()

def main():
	nodes=NodeCollection()
	nodes.load()


	viewer=Viewer(nodes)
	viewer.run()

if __name__ == "__main__":
	main()