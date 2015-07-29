import pygame, random

from NodeCollection import Node, NodeCollection

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
		
		#pick an initial camerax, cameray, zoom factor such that you can see the entire screen
		maxX=max([node.x for node in self.nodeCollection.vertices.values()])
		minX=min([node.x for node in self.nodeCollection.vertices.values()])
		maxY=max([node.y for node in self.nodeCollection.vertices.values()])
		minY=min([node.y for node in self.nodeCollection.vertices.values()])
		#self.camerax=int((maxX+minX)/2)
		#self.cameray=int((maxY+minY)/2)
		#self.zoom=min((maxX-minX)/2, (maxY-minY)/2)
		self.camerax=0
		self.cameray=0
		self.zoom=1.0

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
						update=True
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button==4:	#zoom in
						self.zoom*=1.1
						update=True
					elif event.button==5:
						self.zoom/=1.1
						update=True

			if update:
				screen.fill(BLACK)
				for edge in self.nodeCollection.edges:
					pygame.draw.aalines(screen, RED, True, [
							self.transform(self.nodeCollection[edge[0]].x, self.nodeCollection[edge[0]].y),
							self.transform(self.nodeCollection[edge[1]].x, self.nodeCollection[edge[1]].y)])

				for point in self.nodeCollection.vertices.values():
					pygame.draw.circle(screen, WHITE, self.transform(point.x, point.y), 2)
				
				update=False

			
			clock.tick(30)
			pygame.display.flip()
		

		pygame.quit()

def main():
	nodes=NodeCollection()
	for i in range(400):
		nodes.addNode(i,random.randint(20,800-20),random.randint(20,600-20))

	for i in range(100):
		nodes.addEdge(random.randint(0,99),random.randint(0,99),1)

	viewer=Viewer(nodes)
	viewer.run()

if __name__ == "__main__":
	main()