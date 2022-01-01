
import pygame
import sys
import panel

from pygame.locals import *

screen = pygame.display.set_mode([600 , 400])
panel_example = panel.SList([0 , 0],[200,300])

random_surface = pygame.Surface([400 , 600])
random_surface.fill([138, 28, 28])

surf_2 = pygame.Surface([20 , 600])
surf_2.fill([138, 238, 28])

surf_3 = pygame.Surface([20 , 600])
surf_3.fill([18, 212, 28])

random_surface.blit(surf_2 , [0,0])
random_surface.blit(surf_3 , [350,0])

panel_example.true_surface = random_surface

while True:
     
     screen.fill([20 , 20 , 20])
     
     for event in pygame.event.get():
          if event.type == QUIT:
               pygame.quit()
               sys.exit()
          panel_example.event_handler(event)
     
     panel_example.update()
     
     panel_example.display(screen)
     
     pygame.display.flip()

# # class Foo():
     
# #      def __init__(self):
# #           self.name = 'zefzef'

# # class Foo2():
     
# #      def __init__(self):
# #           self.name = "errerer"

# # foo = Foo()
# # fooBis = Foo2()
# # dic = {foo:fooBis}

# # for key in dic:
# #      print(key)

# # from math import *
# # b = 3
# # a = 2

# # while b - a > 0.1:
     
# #      m = (a+b)/2
     
# #      if exp(m) + exp(-m) - 4*m - 2 > 0:
# #           b = m
# #      else:
# #           a = m

# # print(a , b)

# if len("dede") == 3:
#      print(True)

e = True
z = True
a = e and z
print(a)
e = False
print(a)