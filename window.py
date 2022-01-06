import pygame
import panel
import events

from pygame.locals import *
from ui import *
from panel import *

class Window:
     
     def __init__(self , size):
          
          self.title = "New window"
          
          pos = pygame.display.Info().current_w , pygame.display.Info().current_h
          pos = [pos[0] // 2 - size[0] // 2 , pos[1] // 2 - size[1] // 2]

          self.wb_rect = Rect(pos,[size[0] , 30])
          self.wb_color = [255 , 255 , 255 , 64]
          
          self.surface_rect = Rect([pos[0] , pos[1]+self.wb_rect.height] , size)
          self.surface_color = [100 , 100 , 100]
          
          self.rect = Rect(pos , [self.wb_rect.width+self.surface_rect.width,self.wb_rect.height+self.surface_rect.height])
          
          self.quit_button = Button("quit_window",[self.wb_rect.width - 45 , 0],[45 , 30],{"stringvalue":"X","align center":True} , target_arguments=self)
          self.quit_button.target = events.close_window
          
          self.title_label = Label([20 , 2] , 20 , {"stringValue":self.title,"color":[255 , 255 , 255]})
          
          self.opened = False
          
          self.components = {}
     
     def set_title(self , name : str):
          
          self.title = name
          self.title_label = Label([20 , 2] , 20 , {"stringValue":self.title,"color":[255 , 255 , 255]})
     
     def update(self):
          pass
     
     def quit(self):
          self.opened = False
     
     def event_handler(self , event : pygame.event.Event):
          
          if self.opened:
               
               self.quit_button.event_handler(event , [self.rect.x , self.rect.y])
               
               for component in self.components.values():
                    component.event_handler(event , [self.surface_rect.x , self.surface_rect.y])
     
     def display(self , surface : pygame.Surface):
          
          if self.opened:
               
               final_surface = pygame.Surface(self.rect.size)
               
               wb_surface = pygame.Surface(self.wb_rect.size , SRCALPHA)
               wb_surface.fill(self.wb_color)
               
               self.title_label.display(wb_surface)
               self.quit_button.display(wb_surface)
               
               w_surface = pygame.Surface(self.surface_rect.size , SRCALPHA)
               w_surface.fill(self.surface_color)
               
               for component in self.components.values():
                    component.display(w_surface)
               
               final_surface.blit(wb_surface , [0,0])
               final_surface.blit(w_surface , [0 , self.wb_rect.height])
               
               surface.blit(final_surface , [self.rect.x , self.rect.y])

class File_manager(Window):
     
     def __init__(self):
          super().__init__([550 , 500])
          
          self.set_title("File manager - Open file")
          
          self.components["entry_folderPath"] = Entry("entry_folderPath" , [5 , 50] , [450 , 30],[255 , 255 , 255])
          self.components["entry_folderPath"].default_text = "enter path folder"
          self.components["button_folderPath"] = Button("fp_search",[460 , 50] , [85 , 30],{"stringvalue":"search","align center":True,"color":[255,255,255]})
          self.components["button_folderPath"].target = events.search_files
          
          self.components["FileList_fileFounded"] = Selector_list([5 , 85],[540,350])
          self.components["FileList_fileFounded"].color = [18, 12, 54]
          
          self.components["button_openFile"] = Button("openFile",[460 , 440],[85 , 30],{"stringvalue":"open file","align center":True,"color":[255,255,255]})
          self.components["button_openFile"].target = events.add_file
          
          self.surface_color = [14, 9, 41]
          self.wb_color = [40, 32, 82]
     
     def update(self):
          self.components["FileList_fileFounded"].update()
     
     def load_textures(self):
          
          texture = pygame.Surface([1,1] , SRCALPHA)
          
          texture.fill([58, 42, 142, 0.64*128])
          
          for component in self.components.values():
               
               if isinstance(component , Entry):
                    component.texture = pygame.transform.scale(texture , component.rect.size)
     