import pygame
import scrollbar
import events

from ui import *
from image import *
from pygame.locals import *

class SList():
     
     def __init__(self , pos , size , scrollbar_side=False):
          
          self.rect = Rect([pos[0] , pos[1]] , size)
          
          self.color = [0,0,0]
          
          # self.scrollbar_1 = scrollbar.Scrollbar(self , True)
          self.scrollbar = scrollbar.Scrollbar(self , scrollbar_side)
          
          self.true_surface = pygame.Surface(self.rect.size)
     
     def update(self):
          
          # self.scrollbar_1.update()
          self.scrollbar.update()
          
     def event_handler(self , event , zone_offset=[0,0]):
          
          # self.scrollbar_1.event_handler(event)
          self.scrollbar.event_handler(event , [zone_offset[0],zone_offset[1]])
     
     def display(self , surface):
          
          final_surface = pygame.Surface(self.rect.size)
          final_surface.fill([13, 0, 94])
          
          final_surface.blit(self.true_surface , [0 , self.scrollbar.ts_diff]) if not self.scrollbar.side else final_surface.blit(self.true_surface , [self.scrollbar.ts_diff , 0])
          
          # self.scrollbar_1.draw(final_surface)
          self.scrollbar.display(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])

class Selector_list(SList):
     
     def __init__(self , pos , size , scrollbar_side=False):
          
          super().__init__(pos , size , scrollbar_side)
          
          self.selectors = []
          self.selector_size = 20
     
     def update(self):
          super().update()
     
     def event_handler(self, event , offset=[0,0]):
          super().event_handler(event , offset)
          true_rect = Rect([self.rect.x+offset[0] , self.rect.y+offset[1]],self.rect.size)
          if event.type == (MOUSEBUTTONDOWN or MOUSEBUTTONUP) and not true_rect.collidepoint(event.pos):
               return
          for selector in self.selectors:
               selector.event_handler(event , [self.rect.x+offset[0] , self.rect.y+offset[1]+self.scrollbar.ts_diff] if not self.scrollbar.side else [self.rect.x+offset[0]+self.scrollbar.ts_diff , self.rect.y+offset[1]])
               

     def display(self, surface):
          
          tsh = len(self.selectors) * self.selector_size
          
          true_surface = pygame.Surface([self.rect.width , tsh])
          true_surface.fill(self.color)
          
          for index , selector in enumerate(self.selectors):
               if not self.scrollbar.side:
                    selector.rect.y = index * self.selector_size
               else:
                    selector.rect.x = index * self.selector_size
               selector.display(true_surface)
          
          self.true_surface = true_surface
               
          final_surface = pygame.Surface(self.rect.size)
          final_surface.fill(self.color)
          
          if not self.scrollbar.scrollbar_hid:
               final_surface.blit(self.true_surface , [0 , self.scrollbar.ts_diff]) if not self.scrollbar.side else final_surface.blit(self.true_surface , [self.scrollbar.ts_diff , 0])
               self.scrollbar.display(final_surface)
          else:
               self.scrollbar.ts_diff = 0
               final_surface.blit(self.true_surface , [0 , 0])
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])
          

class Img_displayer_panel():
     
     def __init__(self , pos , size):
          
          self.rect = Rect(pos , size)
          
          self.of_label = Label([self.rect.width // 2 -50 , self.rect.height // 2-20] , 30 , {"stringValue":"No file" , "color":[255 , 255 , 255]})
          self.img_displayer = Img_displayer([0 , 0] , self.rect.size)
          
          self.image_data_backup = []
     
     def update(self):
          
          if self.img_displayer.image.image_loaded:
               self.file_opened = True
          
     def event_handler(self , event):
          
          if self.img_displayer.image.image_loaded:
               self.img_displayer.event_handler(event , [self.rect.x , self.rect.y])
     
     def display(self , surface):
          
          final_surface = pygame.Surface(self.rect.size)
          final_surface.fill([10,10,10])
          
          if not self.img_displayer.image.image_loaded:
               self.of_label.display(final_surface)
          else:
               self.img_displayer.display(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])
               
class UI_panel():
     
     def __init__(self , pos , size):
          
          self.rect = Rect(pos , size)
          self.components = {}
          
          self.texture = pygame.Surface(self.rect.size)
          self.texture.fill([26, 31, 56])
     
     def event_handler(self , event : pygame.event.Event , offset=[0,0]):
          
          for component in self.components.values():
               component.event_handler(event , [self.rect.x+offset[0] , self.rect.y+offset[1]])
     
     def display(self , surface):
          
          final_surface = self.texture.copy()
          
          for component in self.components.values():
               component.display(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])

class Settings_bar(UI_panel):
     
     def __init__(self, pos, size):
          super().__init__(pos, size)
     
     def load_textures(self):
          settings_textures = [pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1]) , SRCALPHA]
          
          settings_textures[0].fill([255, 166, 71, 0.25*128])
          settings_textures[1].fill([255, 166, 71, 0.64*128])
          settings_textures[2].fill([255, 166, 71, 0.9*128])
          
          for component in self.components.values():
               if isinstance(component , Button):
                    component.load_textures(settings_textures)
     

class UI_panel_with_selectors():
     
     def __init__(self , pos , size):
          
          self.rect = Rect(pos , size)
          self.selectors = []
          self.panels = {}
          
          self.texture = pygame.Surface(self.rect.size)
          self.texture.fill([37, 44, 79])
          
          self.actual_panel = None
          
     def create_panel(self , name : str):
          selector = Button([len(self.selectors)*100,0],[100 , 30],{"stringvalue":name,"align center":True , "color":[255 , 255 , 255]} , target_arguments=name)
          selector.target = self.set_panel
          self.selectors.append(selector)
          self.panels[name] = UI_panel([0 , 30] , [self.rect.width , self.rect.height - 30])
     
     def load_textures(self):
          textures = [pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1]) , SRCALPHA]
          
          textures[0].fill([58, 42, 142, 0.25*128])
          textures[1].fill([58, 42, 142, 0.64*128])
          textures[2].fill([58, 42, 142, 0.9*128])
          
          for selector in self.selectors:
               selector.load_textures(textures)
          
          for panel in self.panels.values():
               
               for component in panel.components.values():
               
                    if isinstance(component , Button):
                         component.load_textures(textures)
                    elif isinstance(component , Entry):
                         component.texture = pygame.transform.scale(textures[1] , component.rect.size)
     
     def set_panel(self , name):
          self.actual_panel = self.panels[name]
     
     def event_handler(self , event : pygame.event.Event):
          
          for selector in self.selectors:
               selector.event_handler(event , [self.rect.x , self.rect.y])
          
          if self.actual_panel is not None:     
               self.actual_panel.event_handler(event , [self.rect.x , self.rect.y])
               
     def display(self , surface):
          
          final_surface = self.texture.copy()
          
          for selector in self.selectors:
               selector.display(final_surface)
          
          if self.actual_panel is not None:
               self.actual_panel.display(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])

class Filter_selector(Selector_list):
     
     def __init__(self, pos, size):
          super().__init__(pos, size, True)

          self.selector_size = 150
     
     def add_filter(self , filter_function , name):
          
          selector = Button([len(self.selectors)*150,0],[150 , self.rect.height-20],{"stringvalue":name,"align center":True},filter_function)
          selector.target = events.filter
          self.selectors.append(selector)
     
     def update(self):
          return super().update()
     
     def event_handler(self, event, offset=[0, 0]):
          return super().event_handler(event, offset=offset)
     
     def display(self, surface):
          return super().display(surface)


          