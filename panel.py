import pygame
import scrollbar

from ui import *
from pygame.locals import *

class SList():
     
     def __init__(self , pos , size , offset=[0,0]):
          
          self.rect = Rect([pos[0]+offset[0] , pos[1]+offset[1]] , size)
          
          self.scrollbar = scrollbar.Scrollbar(self)
          
          self.true_surface = pygame.Surface(self.rect.size)
          self.true_surface.fill([40 , 40 , 40])
          
          self.scrollbar_hid = False
     
     def update(self):
          
          self.scrollbar.update()
          
     def event_handler(self , event):
          
          self.scrollbar.event_handler(event)
     
     def display(self , surface):
          
          final_surface = pygame.Surface(self.rect.size)
          final_surface.fill([100 , 100 , 100])
          final_surface.blit(self.true_surface , [0 , self.scrollbar.y_ts_diff])
          
          self.scrollbar.draw(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])

class File_list(SList):
     
     def __init__(self , pos , size , offset=[0,0]):
          
          super().__init__(pos , size , offset)
          
          self.files = []
     
     def update(self):
          super().update()
     
     def event_handler(self, event):
          super().event_handler(event)
          
          if event.type == (MOUSEBUTTONDOWN or MOUSEBUTTONUP) and not self.rect.collidepoint(event.pos):
               return
          
          for selector in self.files:
               selector.event_handler(event , [self.true_surface.get_rect().x+self.rect.x , self.rect.y+self.scrollbar.y_ts_diff])
               

     def display(self, surface):
          
          tsh = len(self.files) * 26
          
          true_surface = pygame.Surface([self.rect.width , tsh])
          
          for index , selector in enumerate(self.files):
               selector.rect.y = index * 26
               selector.display(true_surface)
          
          self.true_surface = true_surface
               
          final_surface = pygame.Surface(self.rect.size)
          final_surface.fill([120 , 120 , 120])
          final_surface.blit(self.true_surface , [0 , self.scrollbar.y_ts_diff])
          
          self.scrollbar.draw(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])
          

class Img_displayer_panel():
     
     def __init__(self , pos , size):
          
          self.rect = Rect(pos , size)
          
          self.of_button = Button([self.rect.width // 2 -50 , self.rect.height // 2-20] , [100 , 40] , {"stringvalue":"Open image","align center":True})
          self.of_button.target = events.load_image_test
          self.img_displayer = Img_displayer([0 , 0] , self.rect.size)
     
     def update(self):
          
          if self.img_displayer.image.image_loaded:
               self.file_opened = True
          
     def event_handler(self , event):
          
          if not self.img_displayer.image.image_loaded:
               self.of_button.event_handler(event , [self.rect.x , self.rect.y])
          else:
               self.img_displayer.event_handler(event , [self.rect.x , self.rect.y])
     
     def display(self , surface):
          
          final_surface = pygame.Surface(self.rect.size)
          final_surface.fill([10,10,10])
          
          if not self.img_displayer.image.image_loaded:
               self.of_button.display(final_surface)
          else:
               self.img_displayer.display(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])
          
          