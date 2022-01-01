import pygame
import scrollbar

from ui import *
from image import *
from pygame.locals import *

class SList():
     
     def __init__(self , pos , size , offset=[0,0] , scrollbar_side=False):
          
          self.rect = Rect([pos[0]+offset[0] , pos[1]+offset[1]] , size)
          
          self.color = [0,0,0]
          
          # self.scrollbar_1 = scrollbar.Scrollbar(self , True)
          self.scrollbar_2 = scrollbar.Scrollbar(self , False)
          
          self.true_surface = pygame.Surface(self.rect.size)
     
     def update(self):
          
          # self.scrollbar_1.update()
          self.scrollbar_2.update()
          
     def event_handler(self , event , zone_offset=[0,0]):
          
          # self.scrollbar_1.event_handler(event)
          self.scrollbar_2.event_handler(event , [zone_offset[0],zone_offset[1]])
     
     def display(self , surface):
          
          final_surface = pygame.Surface(self.rect.size)
          final_surface.fill([13, 0, 94])
          
          final_surface.blit(self.true_surface , [0 , self.scrollbar_2.ts_diff])
          
          # self.scrollbar_1.draw(final_surface)
          self.scrollbar_2.display(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])

class Image_list(SList):
     
     def __init__(self , pos , size , offset=[0,0]):
          
          super().__init__(pos , size , offset)
          
          self.files = []
     
     def update(self):
          super().update()
     
     def event_handler(self, event , offset=[0,0]):
          super().event_handler(event , offset)
          
          if event.type == (MOUSEBUTTONDOWN or MOUSEBUTTONUP) and not self.rect.collidepoint(event.pos):
               return
          
          for selector in self.files:
               selector.event_handler(event , [self.true_surface.get_rect().x+self.rect.x+offset[0] , self.rect.y+self.scrollbar_2.ts_diff+offset[1]])
               

     def display(self, surface):
          
          tsh = len(self.files) * 20
          
          true_surface = pygame.Surface([self.rect.width , tsh])
          true_surface.fill(self.color)
          
          for index , selector in enumerate(self.files):
               selector.rect.y = index * 20
               selector.display(true_surface)
          
          self.true_surface = true_surface
               
          final_surface = pygame.Surface(self.rect.size)
          final_surface.fill(self.color)
          
          if not self.scrollbar_2.scrollbar_hid:
               final_surface.blit(self.true_surface , [0 , self.scrollbar_2.ts_diff])
               self.scrollbar_2.display(final_surface)
          else:
               self.scrollbar_2.ts_diff = 0
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
          self.selectors = {}
          self.panels = {}
          
          self.texture = pygame.Surface(self.rect.size)
          self.texture.fill([37, 44, 79])
          
          self.selectors["main tools"] = Button([0,0],[100 , 30],{"stringvalue":"Main tools","align center":True , "color":[255 , 255 , 255]})
          
          self.panels["main tools"] = UI_panel([0 , 30] , [self.rect.width , self.rect.height - 30])
          self.actual_panels = self.panels["main tools"]
          
          self.panels["main tools"].components["button_SymHori"] = Button([10, 5] , [200 , 30] , {"stringvalue":"Horizontal symmetry","align center":True,"color":[255 , 255 , 255]})
          self.panels["main tools"].components["button_SymHori"].target = events.sym_hori
          
          self.panels["main tools"].components["button_SymVert"] = Button([10,40] , [200 , 30] , {"stringvalue":"Vertical symmetry","align center":True,"color":[255 , 255 , 255]})
          self.panels["main tools"].components["button_SymVert"].target = events.sym_vert

          self.panels["main tools"].components["button_rot180"] = Button([10,75] , [200 , 30] , {"stringvalue":"Rotation 180°","align center":True,"color":[255 , 255 , 255]})
          self.panels["main tools"].components["button_rot180"].target = events.rot_180
          
          self.panels["main tools"].components["button_rot90"] = Button([10,110] , [200 , 30] , {"stringvalue":"Rotation 90°","align center":True,"color":[255 , 255 , 255]})
          self.panels["main tools"].components["button_rot90"].target = events.rot_90
          
          self.panels["main tools"].components["button_convPGM"] = Button([240,5] , [120 , 30] , {"stringvalue":"To PGM","align center":True,"color":[255 , 255 , 255]})
          self.panels["main tools"].components["button_convPGM"].target = events.pgm_conv
          
          self.panels["main tools"].components["button_convPBM"] = Button([240,40] , [120 , 30] , {"stringvalue":"To PBM :","align center":True,"color":[255 , 255 , 255]})
          self.panels["main tools"].components["button_convPBM"].target = events.pbm_conv  
          
          self.panels["main tools"].components["entry_intConvPBM"] =  Entry("entry_intConvPBM", [370 , 40] , [120 , 30] , [255 , 255 , 255])
          self.panels["main tools"].components["entry_intConvPBM"].default_text = "Intensity - %"   
          self.panels["main tools"].components["entry_intConvPBM"].max_lenght = 3
          self.panels["main tools"].components["entry_intConvPBM"].extra_string = "%" 
          
          self.panels["main tools"].components["button_lum"] = Button([240,75] , [120 , 30] , {"stringvalue":"brightness :","align center":True,"color":[255 , 255 , 255]})
          self.panels["main tools"].components["button_lum"].target = events.luminosity
          
          self.panels["main tools"].components["entry_luminance"] =  Entry("entry_luminance", [370 , 75] , [120 , 30] , [255 , 255 , 255])
          self.panels["main tools"].components["entry_luminance"].default_text = "Luminance - %"   
          self.panels["main tools"].components["entry_luminance"].max_lenght = 3
          self.panels["main tools"].components["entry_luminance"].extra_string = "%" 
          
          self.panels["main tools"].components["button_saturation"] = Button([240,110] , [120 , 30] , {"stringvalue":"saturate :","align center":True,"color":[255 , 255 , 255]})
          self.panels["main tools"].components["button_saturation"].target = events.saturation
          
          self.panels["main tools"].components["entry_saturation"] =  Entry("entry_saturation", [370 , 110] , [120 , 30] , [255 , 255 , 255])
          self.panels["main tools"].components["entry_saturation"].default_text = "saturation - %"   
          self.panels["main tools"].components["entry_saturation"].max_lenght = 3
          self.panels["main tools"].components["entry_saturation"].extra_string = "%" 
          
          self.panels["main tools"].components["button_rotation"] = Button([520,5] , [120 , 30] , {"stringvalue":"rotate :","align center":True,"color":[255 , 255 , 255]})
          self.panels["main tools"].components["button_rotation"].target = events.rotation
          
          self.panels["main tools"].components["entry_rotation"] =  Entry("entry_rotation", [650 , 5] , [120 , 30] , [255 , 255 , 255])
          self.panels["main tools"].components["entry_rotation"].default_text = "rotation - °"   
          self.panels["main tools"].components["entry_rotation"].max_lenght = 3
          self.panels["main tools"].components["entry_rotation"].extra_string = "°" 
          
          self.panels["main tools"].components["button_resize"] = Button([520,50] , [120 , 30] , {"stringvalue":"resize :","align center":True,"color":[255 , 255 , 255]})
          # self.panels["main tools"].components["button_resize"].target = ?
          
          self.panels["main tools"].components["entry_xSize"] =  Entry("entry_xSize", [650 , 50] , [120 , 30] , [255 , 255 , 255])
          self.panels["main tools"].components["entry_xSize"].default_text = "X - pixel"   
          self.panels["main tools"].components["entry_xSize"].max_lenght = 4
          self.panels["main tools"].components["entry_xSize"].extra_string = "px" 
          
          self.panels["main tools"].components["entry_ySize"] =  Entry("entry_ySize", [650 , 85] , [120 , 30] , [255 , 255 , 255])
          self.panels["main tools"].components["entry_ySize"].default_text = "Y - pixel"   
          self.panels["main tools"].components["entry_ySize"].max_lenght = 4
          self.panels["main tools"].components["entry_ySize"].extra_string = "px" 
          
          self.panels["main tools"].components["button_undo"] = Button([850,0] , [50 , 30] , {"stringvalue":"undo","align center":True,"color":[255 , 255 , 255]})
          self.panels["main tools"].components["button_undo"].target = events.undo
     
     def load_textures(self):
          textures = [pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1]) , SRCALPHA]
          
          textures[0].fill([58, 42, 142, 0.25*128])
          textures[1].fill([58, 42, 142, 0.64*128])
          textures[2].fill([58, 42, 142, 0.9*128])
          
          for selector in self.selectors.values():
               selector.load_textures(textures)
          
          for component in self.panels["main tools"].components.values():
               
               if isinstance(component , Button):
                    component.load_textures(textures)
               elif isinstance(component , Entry):
                    component.texture = pygame.transform.scale(textures[1] , component.rect.size)
     
     
     def event_handler(self , event : pygame.event.Event):
          
          for selector in self.selectors.values():
               selector.event_handler(event , [self.rect.x , self.rect.y])
               
          self.actual_panels.event_handler(event , [self.rect.x , self.rect.y])
               
     def display(self , surface):
          
          final_surface = self.texture.copy()
          
          for selector in self.selectors.values():
               selector.display(final_surface)
          
          self.actual_panels.display(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])


          