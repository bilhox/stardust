import pygame
import traitement
import events

from pygame.locals import *
from ui import *
from panel import *

class Window:
     
     WINDOW_CLOSED = USEREVENT+1
     
     def __init__(self , size):
          
          self.title = "New window"
          
          pos = pygame.display.Info().current_w , pygame.display.Info().current_h
          pos = [pos[0] // 2 - size[0] // 2 , pos[1] // 2 - size[1] // 2]

          self.wb_rect = Rect(pos,[size[0] , 30])
          
          self.surface_rect = Rect([pos[0] , pos[1]+self.wb_rect.height] , size)
          
          self.rect = Rect(pos , [self.wb_rect.width+self.surface_rect.width,self.wb_rect.height+self.surface_rect.height])
          
          self.quit_button = Button("quit_window",[self.wb_rect.width - 45 , 0],[45 , 30],{"stringvalue":"X","align center":True},pygame.event.Event(Window.WINDOW_CLOSED , {"window":self}))
          self.quit_button.target = pygame.event.post
          
          self.title_label = Label([20 , 3] , 20 , {"stringValue":self.title,"color":[255 , 255 , 255]})
          
          self.opened = False
          
          self.components = {}
          
          self.wb_texture = pygame.Surface(self.wb_rect.size , SRCALPHA)
          self.texture = pygame.Surface(self.surface_rect.size , SRCALPHA)   
          self.texture.fill([100,100,100])
          self.wb_texture.fill([255 , 255 , 255 , 100])
     
     def start(self):
          pass
            
     def set_title(self , name : str):
          
          self.title = name
          self.title_label = Label([20 , 2] , 20 , {"stringValue":self.title,"color":[255 , 255 , 255]})
     
     def update(self):
          pass
     
     def quit(self):
          self.opened = False
     
     def set_color(self , wb_color , surface_color):
          self.texture.fill(surface_color)
          self.wb_texture.fill(wb_color)
     
     def event_handler(self , event : pygame.event.Event):
          
          if self.opened:
               
               self.quit_button.event_handler(event , [self.rect.x , self.rect.y])
               
               for component in self.components.values():
                    component.event_handler(event , [self.surface_rect.x , self.surface_rect.y])
     
     def display(self , surface : pygame.Surface):
          
          if self.opened:
               
               final_surface = pygame.Surface(self.rect.size)
               
               wb_surface = pygame.transform.scale(self.wb_texture.copy(), self.wb_rect.size)
               
               self.title_label.display(wb_surface)
               self.quit_button.display(wb_surface)
               
               w_surface = pygame.transform.scale(self.texture.copy(), self.surface_rect.size)
               
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
          
          self.set_color([40, 32, 82],[14, 9, 41])
     
     def update(self):
          self.components["FileList_fileFounded"].update()
     
     def load_textures(self):
          
          texture = pygame.Surface([1,1] , SRCALPHA)
          
          texture.fill([58, 42, 142, 0.64*128])
          
          for component in self.components.values():
               
               if isinstance(component , Entry):
                    component.texture = pygame.transform.scale(texture , component.rect.size)

class RC_window(Window):
     
     def __init__(self , image_displayer : Img_displayer):
          super().__init__([800 , 500])
          
          self.app_ID = image_displayer
          
          self.components["Img displayer"] = Img_displayer([5,5],[640 , 490])
          
          self.components["entry_value"] = Entry("value",[650 , 5],[145 , 40],[255,255,255])
          self.components["entry_value"].max_lenght = 3
          self.components["entry_value"].default_text = "Intensity - %"
          self.components["entry_value"].extra_string = "%"
          
          self.components["button_renderChanges"] = Button("applyChanges",[650,50],[145 , 40],{"stringvalue":"render changes","align center":True,"color":[255,255,255]})
          self.components["button_renderChanges"].target = self.update_image
          
          self.components["button_applyChanges"] = Button("applyChanges",[650,450],[145 , 40],{"stringvalue":"apply changes","align center":True,"color":[255,255,255]})
          self.components["button_applyChanges"].target = None
          self.components["button_applyChanges"].target_arguments = {"value":0,"img_displayer":self.app_ID,"window":self}
          
          self.traitement = None
          
          self.set_color([40, 32, 82],[14, 9, 41])
     
     def start(self):
          if self.app_ID.image.image_loaded:
               self.components["Img displayer"].image.load_by_data(self.app_ID.image.image_data , False)
          else:
               self.components["Img displayer"].image = Image([0,0])
               
     
     def update_image(self):
          try:
               self.components["Img displayer"].image.load_by_data(self.traitement(self.app_ID.image.image_data,int(self.components["entry_value"].stringValue)),False)
               self.components["button_applyChanges"].target_arguments = {"value":int(self.components["entry_value"].stringValue),"img_displayer":self.app_ID,"window":self}
          except:
               pass
          
              
     