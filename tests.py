# import pygame
# import sys
# import panel

# from pygame.locals import *

# screen = pygame.display.set_mode([600 , 400])
# panel_example = panel.SList([0 , 30],[200,380])

# random_surface = pygame.Surface([600 , 1600])
# random_surface.fill([21 , 234 , 63])

# another_surface = pygame.Surface([600 , 400])
# another_surface.fill([239 , 90 , 12])

# random_surface.blit(another_surface , [0 , 400])

# panel_example.true_surface = random_surface

# while True:
     
#      screen.fill([20 , 20 , 20])
     
#      for event in pygame.event.get():
#           if event.type == QUIT:
#                pygame.quit()
#                sys.exit()
#           panel_example.event_handler(event)
     
#      panel_example.update()
     
#      panel_example.display(screen)
     
#      pygame.display.flip()

class Foo():
     
     def __init__(self):
          self.name = 'zefzef'

class Foo2():
     
     def __init__(self):
          self.name = "errerer"

foo = Foo()
fooBis = Foo2()
dic = {foo:fooBis}

for key in dic:
     print(key)