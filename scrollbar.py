import pygame

from pygame.locals import *

class Scrollbar:
     
     def __init__(self , panel):
          
          self.scroll_rect = Rect([panel.rect.width - 20 , 0],[20 , panel.rect.height])
          self.bar_rect = Rect([self.scroll_rect.x , self.scroll_rect.y] , [20 , 50])
     
          self.on_bar = False
          self.panel_ref = panel
          self.mouse_diff = 0
          
          #y true surface difference
          self.y_ts_diff = 0
     
     def update(self):
          
          # panel_true_surface_height
          ptsh = self.panel_ref.true_surface.get_rect().height
          self.bar_rect.height = int(self.scroll_rect.height / (ptsh / self.scroll_rect.height))
          
          bar_half_lenght = self.bar_rect.height / 2
          scroll_lenght = self.scroll_rect.height - self.bar_rect.height
          height_diff = ptsh - self.scroll_rect.height
          
          if self.y_ts_diff > 0:
               self.y_ts_diff = 0
          elif self.y_ts_diff + ptsh < self.panel_ref.rect.height:
               self.y_ts_diff = height_diff
          
          if self.on_bar:
               mouse_pos = pygame.mouse.get_pos()
               self.bar_rect.y = mouse_pos[1] - self.mouse_diff
               
               if self.bar_rect.y < self.scroll_rect.y:
                    self.bar_rect.y = 0
               elif self.bar_rect.bottom > self.scroll_rect.bottom:
                    self.bar_rect.bottom = self.scroll_rect.bottom
               
               self.y_ts_diff = int((height_diff / scroll_lenght) * (self.bar_rect.centery - bar_half_lenght) * -1)
     
     def event_handler(self , event):
           
          if event.type == MOUSEBUTTONDOWN:
               if self.bar_rect.collidepoint(event.pos):
                    self.on_bar = True
                    self.mouse_diff = event.pos[1] - self.bar_rect.top
          if event.type == MOUSEBUTTONUP:
               self.on_bar = False
               self.mouse_diff = 0
     
     def draw(self , surface):
          
          pygame.draw.rect(surface, [150 , 150 , 150], self.scroll_rect)
          pygame.draw.rect(surface, [50 , 50 , 50], self.bar_rect)