import pygame

from pygame.locals import *

class Scrollbar:
     
     def __init__(self , panel):
          
          self.panel_ref = panel
          
          self.scroll_rect = Rect([self.panel_ref.rect.width - 20 , 0],[20 , self.panel_ref.rect.height])
          self.bar_rect = Rect([self.scroll_rect.x , self.scroll_rect.y] , [20 , 50])
     
          self.on_bar = False
          self.mouse_diff = 0
          
          #y true surface difference
          self.y_ts_diff = 0
          self.change_y = 0
     
     def update(self):
          
          self.y_ts_diff += self.change_y
          
          # panel_true_surface_height
          ptsh = self.panel_ref.true_surface.get_rect().height
          height_diff = ptsh - self.scroll_rect.height
          
          if self.y_ts_diff > 0:
               self.y_ts_diff = 0
          elif self.y_ts_diff + ptsh < self.panel_ref.rect.height:
               self.y_ts_diff = height_diff
          
          self.bar_rect.height = int(self.scroll_rect.height / (ptsh / self.scroll_rect.height))
          
          bar_half_lenght = self.bar_rect.height / 2
          scroll_length = self.scroll_rect.height - self.bar_rect.height
          
          if self.on_bar:
               mouse_pos = pygame.mouse.get_pos()
               self.bar_rect.y = mouse_pos[1] - self.mouse_diff
               
               if self.bar_rect.y < self.scroll_rect.y:
                    self.bar_rect.y = 0
               elif self.bar_rect.bottom > self.scroll_rect.height:
                    self.bar_rect.bottom = self.scroll_rect.height
               
               self.y_ts_diff = int((height_diff / scroll_length) * (self.bar_rect.centery - bar_half_lenght) * -1)
          else:
               self.bar_rect.centery =  scroll_length / (height_diff * 1.0) * (self.y_ts_diff * -1) + bar_half_lenght
     
     def event_handler(self , event):
           
          if event.type == MOUSEBUTTONDOWN:
               if event.button == 1:
                    if self.bar_rect.collidepoint([event.pos[0]-self.panel_ref.rect.x , event.pos[1]-self.panel_ref.rect.y]):
                         self.on_bar = True
                         self.mouse_diff = event.pos[1] - self.bar_rect.top
          if event.type == MOUSEBUTTONUP:
               self.on_bar = False
          
          # if event.type == KEYDOWN:
          #      if event.key == K_UP:
          #           self.change_y = 5
          #      elif event.key == K_DOWN:
          #           self.change_y = -5
                
          # if event.type == KEYUP:
          #      if event.key == K_UP:
          #           self.change_y = 0
          #      elif event.key == K_DOWN:
          #           self.change_y = 0
     
     def draw(self , surface):
          
          pygame.draw.rect(surface, [150 , 150 , 150], self.scroll_rect)
          pygame.draw.rect(surface, [50 , 50 , 50], self.bar_rect)