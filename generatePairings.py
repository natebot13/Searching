def generate_square_grid_graph(n):
  w = int(n**0.5)
  for y in range(w):
    for x in range(y * w, y * w + w - 1):
      yield (x, x + 1)
  for y in range(w - 1):
    for x in range(y * w, y * w + w):
      yield (x, x + w)

types = {'grid': generate_square_grid_graph}

def create_file(f, n):
  with open('pairings.txt', 'w') as pfile:
    pfile.write(str(n) + '\n')
    for a, b in f(n):
      pfile.write(str(a) + ',' + str(b) + '\n')

def main():
  running = True
  print("Generate a graph file.")
  while running:
    print("Options:")
    for key in types:
      print(key)
    choice = input('>>> ')
    if choice in types:
      print('How many nodes?')
      NaN = True
      while NaN:
        try:
          num = int(input('>>> '))
          create_file(types[choice], num)
          print('File created.')
          NaN = False
          running = False
        except ValueError:
          print('Not a number.')
    else:
      print('Invalid option. Try again.')

if __name__ == '__main__':
  main()