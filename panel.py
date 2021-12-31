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
          
          self.scrollbar_hid = False
     
     def update(self):
          
          # self.scrollbar_1.update()
          self.scrollbar_2.update()
          
     def event_handler(self , event):
          
          # self.scrollbar_1.event_handler(event)
          self.scrollbar_2.event_handler(event)
     
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
     
     def event_handler(self, event):
          super().event_handler(event)
          
          if event.type == (MOUSEBUTTONDOWN or MOUSEBUTTONUP) and not self.rect.collidepoint(event.pos):
               return
          
          for selector in self.files:
               selector.event_handler(event , [self.true_surface.get_rect().x+self.rect.x , self.rect.y+self.scrollbar_2.ts_diff])
               

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
          
          if not self.scrollbar_hid:
               final_surface.blit(self.true_surface , [0 , self.scrollbar_2.ts_diff])
          else:
               self.scrollbar_2.ts_diff = 0
               final_surface.blit(self.true_surface , [0 , 0])
          
          self.scrollbar_2.display(final_surface)
          
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


class Window_panel:
     
     def __init__(self , size):
          
          self.title = "New window"
          
          pos = pygame.display.Info().current_w , pygame.display.Info().current_h
          pos = [pos[0] // 2 - size[0] // 2 , pos[1] // 2 - size[1] // 2]

          self.wb_rect = Rect(pos,[size[0] , 30])
          self.wb_color = [255 , 255 , 255 , 64]
          
          self.surface_rect = Rect([pos[0] , pos[1]+self.wb_rect.height] , size)
          self.surface_color = [100 , 100 , 100]
          
          self.quit_button = Button([self.wb_rect.width - 45 , 0],[45 , 30],{"stringvalue":"X","align center":True} , target_arguments=self)
          self.quit_button.target = events.close_window
          
          self.title_label = Label([20 , 2] , 20 , {"stringValue":self.title,"color":[255 , 255 , 255]})
          
          self.opened = False
     
     def quit(self):
          self.opened = False
     
     def event_handler(self , event : pygame.event.Event):
          
          if self.opened:
               
               self.quit_button.event_handler(event , [self.wb_rect.x , self.wb_rect.y])
     
     def display(self , surface : pygame.Surface):
          
          if self.opened:
               
               final_surface = pygame.Surface([self.surface_rect.w , self.surface_rect.h  + self.wb_rect.h])
               
               wb_surface = pygame.Surface(self.wb_rect.size , SRCALPHA)
               wb_surface.fill(self.wb_color)
               
               self.title_label.display(wb_surface)
               self.quit_button.display(wb_surface)
               
               w_surface = pygame.Surface(self.surface_rect.size , SRCALPHA)
               w_surface.fill(self.surface_color)
               
               final_surface.blit(wb_surface , [0,0])
               final_surface.blit(w_surface , [0 , self.wb_rect.height])
               
               surface.blit(final_surface , [self.wb_rect.x , self.wb_rect.y])
               
class UI_panel():
     
     def __init__(self , pos , size):
          
          self.rect = Rect(pos , size)
          self.components = {}
          
          self.texture = pygame.Surface(self.rect.size)
          self.texture.fill([26, 31, 56])
     
     def load_textures(self , textures):
          
          for component in self.components.values():
               
               if isinstance(component , Button):
                    component.load_textures(textures)
               elif isinstance(component , Entry):
                    component.texture = pygame.transform.scale(textures[0] , component.rect.size)
     
     def event_handler(self , event : pygame.event.Event , offset=[0,0]):
          
          for component in self.components.values():
               component.event_handler(event , [self.rect.x+offset[0] , self.rect.y+offset[1]])
     
     def display(self , surface):
          
          final_surface = self.texture.copy()
          
          for component in self.components.values():
               component.display(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])
     

class UI_panel_with_selectors():
     
     def __init__(self , pos , size):
          
          self.rect = Rect(pos , size)
          self.selectors = {}
          self.panels = {}
          
          self.texture = pygame.Surface(self.rect.size)
          self.texture.fill([37, 44, 79])
          
          self.selectors["main tools"] = Button([0,0],[100 , 30],{"stringvalue":"Main tools","align center":True , "color":[255 , 255 , 255]})
          
          textures = [pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1]) , SRCALPHA]
          
          textures[0].fill([58, 42, 142, 0.25*128])
          textures[1].fill([58, 42, 142, 0.64*128])
          textures[2].fill([58, 42, 142, 0.9*128])
          
          for selector in self.selectors.values():
               selector.load_textures(textures)
          
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
          
          self.panels["main tools"].load_textures(textures)
     
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


          