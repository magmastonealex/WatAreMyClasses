import pygame, random

"""Draws vertices and edges to the screen. Currently randomly generates vertices and edges.
Hold left mouse button down and drag to pan.
Scroll mouse wheel to zoom in and out."""

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
WIDTH = 800
HEIGHT = 600

from . import node

nodes=NodeCollection()
nodes.addNode(1,2,3,name="hello")

def main():
	zoom=1.0	#higher zoom = things look bigger
	camerax=0
	cameray=0
	
	pygame.init()

	size = (WIDTH, HEIGHT)
	screen = pygame.display.set_mode(size)
	
	pygame.display.set_caption("map data visualizer")

	nodes=NodeCollection()
	for i in range(100):
		nodes.addNode(i,random.randint(20,WIDTH-20),random.randint(20,HEIGHT-20))

	for i in range(100):
		nodes.addEdge(random.randint(0,99),random.randint(0,99),1)

	run=True
	clock = pygame.time.Clock()
	update=True

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.MOUSEMOTION:
				if event.buttons[0]:
					camerax-=event.rel[0]/zoom
					cameray-=event.rel[1]/zoom
					update=True
					print camerax,cameray
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button==4:	#zoom in
					zoom*=1.1
					update=True
				elif event.button==5:
					zoom/=1.1
					update=True

		if update:
			screen.fill(BLACK)
			for edge in nodes.edges:
				pygame.draw.aalines(screen, RED, True, [
						transform(nodes[edge[0]].x,nodes[edge[0]].y, zoom, camerax, cameray),
						transform(nodes[edge[1]].x,nodes[edge[1]].y, zoom, camerax, cameray)])

			for point in nodes.vertices:
				pygame.draw.circle(screen, WHITE, transform(nodes[point].x,nodes[point].y, zoom, camerax, cameray),2)
			
			update=False

		
		clock.tick(30)
		pygame.display.flip()
	

	pygame.quit()

if __name__ == "__main__":
	main()