import pygame

class node:
  def __init__(self, cost):
    self.cost = cost
    self.visited = False
    self.neighbors = []
    self.selected = False
    self.onPath = False

  def addNeighbor(self, n):
    self.neighbors.append(n)

  def draw(self, screen, x, y, w):
    color = pygame.Color(0,0,0)
    color.hsva = (self.cost % 360, 100, 100, 100)
    if self.selected:
      color = (255,255,255)
      self.selected = False
    rect = pygame.Rect(x, y, w, w)
    # print(color)
    pygame.draw.rect(screen, color, rect, 2)
    if self.visited:
      center = (x + w//2, y + w//2)
      color = (255,255,255)
      if self.onPath:
        color = (0,255,0)
      pygame.draw.circle(screen, color, center, (w//2)-4)

  def select(self):
    self.selected = True

  def visit(self):
    self.visited = not self.visited

  def setOnPath(self):
    self.onPath = True

class terrain:
  def __init__(self, numNodes, pairings):
    self.nodes = []
    for i in range(numNodes):
      self.nodes.append(node(i))
    for a,b in pairings:
      self.nodes[a].addNeighbor(self.nodes[b])
      self.nodes[b].addNeighbor(self.nodes[a])

  def drawSquareTerrain(self, screen, w, nodew):
    for i, n in enumerate(self.nodes):
      y = i // w
      x = i % w
      n.draw(screen, x * nodew, y * nodew, nodew)

  def selectNodeAndNeighbors(self, w, nodew, pos):
    if not pos: return
    x, y = pos
    nodei = (y // nodew) * w + (x // nodew)
    n = self.nodes[nodei]
    n.select()
    for neigh in n.neighbors:
      neigh.select()

  def getNode(self, i):
    return self.nodes[i]

class searcher:
  queue = set()
  target = None
  def init(s, t):
    s.prev = None
    searcher.queue = [s]
    searcher.target = t

  def bfs():
    level = set()
    while searcher.queue:
      n = searcher.queue.pop()
      n.visit()
      if n is searcher.target:
        n.setOnPath()
        while n.prev:
          n = n.prev
          n.setOnPath()
        searcher.queue = set()
        return;
      for each in n.neighbors:
        if not each.visited:
          level.add(each)
          each.prev = n
    searcher.queue = level


def main(search=searcher.bfs):
  WIDTH = 500
  HEIGHT = 500
  SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
  CLOCK = pygame.time.Clock()
  FPS = 2

  pairings = []
  with open('pairings.txt', 'r') as p:
    numNodes = int(p.readline().strip())
    for line in p:
      line = line.strip()
      pair = (int(i) for i in line.split(','))
      pairings.append(pair)

  t = terrain(numNodes, pairings)
  mousePos = None

  searcher.init(t.getNode(0), t.getNode(190))

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.MOUSEMOTION:
        mousePos = event.pos

    search()

    TerrainWxH = int(numNodes**0.5)
    t.selectNodeAndNeighbors(TerrainWxH, WIDTH//TerrainWxH, mousePos)
    t.drawSquareTerrain(SCREEN, TerrainWxH, WIDTH//TerrainWxH)
    pygame.display.update()
    CLOCK.tick(FPS)

if __name__ == '__main__':
  main()