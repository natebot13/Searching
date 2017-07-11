import pygame

class node:
  def __init__(self, value):
    self.value = value
    self.visited = False
    self.neighbors = []
    self.selected = False
    self.onPath = False

  def addNeighbor(self, n):
    self.neighbors.append(n)

  def draw(self, screen, x, y, w):
    x = round(x)
    y = round(y)
    w = round(w)
    color = pygame.Color(0,0,255)
    if self.selected:
      color = (150,150,255)
      self.selected = False
    rect = pygame.Rect(x, y, w, w)
    # print(color)
    pygame.draw.rect(screen, color, rect)
    if self.visited:
      center = (x + w//2, y + w//2)
      color = (100,100,255)
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
    self.edges = {}
    for i in range(numNodes):
      self.nodes.append(node(i))
    for a,b,c in pairings:
      self.nodes[a].addNeighbor(self.nodes[b])
      self.nodes[b].addNeighbor(self.nodes[a])
      self.edges[(a,b)] = c

  def drawSquareTerrain(self, screen, w, nodew, spacing):
    nodew = nodew//spacing
    wheretheyat = {}
    for i, n in enumerate(self.nodes):
      y = i // w
      x = i % w
      actualX = x * spacing * nodew + (nodew // 2)
      actualY = y * spacing * nodew + (nodew // 2)
      n.draw(screen, actualX, actualY, nodew)
      wheretheyat[i] = (actualX + nodew // 2, actualY + nodew // 2)
    for edge, cost in self.edges.items():
      a,b = edge
      color = (0,0,255)
      thickness = 2
      nodea = self.nodes[a]
      nodeb = self.nodes[b]
      if nodea.onPath and nodeb.onPath and (nodea.prev is nodeb or nodeb.prev is nodea):
        color = (0,255,0)
        thickness = 10
      pygame.draw.line(screen, color, wheretheyat[a], wheretheyat[b], thickness)


  def drawTreeTerrain(self, screen, width, height):
    pass

  def selectNodeAndNeighbors(self, w, nodew, pos):
    if not pos: return
    x, y = pos
    nodei = (y  // nodew) * w + (x // nodew)
    n = self.nodes[nodei]
    n.select()
    for neigh in n.neighbors:
      neigh.select()

  def getNode(self, i):
    return self.nodes[i]

class searcher:
  queue = []
  target = None
  def init(s, t):
    s.prev = None
    searcher.queue = [s]
    searcher.target = t
    searcher.level = set()

  def bfs():
    if searcher.queue is None or searcher.level is None:
      return
    if searcher.queue:
      n = searcher.queue.pop()
      n.visit()
      if n is searcher.target:
        n.setOnPath()
        while n.prev:
          n = n.prev
          n.setOnPath()
        searcher.queue = None
        searcher.level = None
        return;
      for each in n.neighbors:
        if not each.visited:
          each.select()
          searcher.level.add(each)
          each.prev = n
    else:
      searcher.queue = [n for n in searcher.level]
      searcher.level = set()

  def dfs():
    if searcher.queue:
      n = searcher.queue.pop()
      n.visit()
      if n is searcher.target:
        n.setOnPath()
        while n.prev:
          n = n.prev
          n.setOnPath()
        searcher.queue = []
      for each in n.neighbors:
        if not each.visited:
          each.select()
          searcher.queue.append(each)
          each.prev = n

def main(search=searcher.bfs):
  WIDTH = 1000
  HEIGHT = 1000
  SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
  CLOCK = pygame.time.Clock()
  FPS = 40

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
    spacingScale = 1.5
    # t.selectNodeAndNeighbors(TerrainWxH, WIDTH//TerrainWxH, mousePos)
    SCREEN.fill((0,0,150))
    t.drawSquareTerrain(SCREEN, TerrainWxH, WIDTH//TerrainWxH, spacingScale)
    pygame.display.update()
    CLOCK.tick(FPS)

if __name__ == '__main__':
  main()