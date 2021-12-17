import pygame
import events

from components import *


class Package():
     
     def __init__(self , title : str , pos : list , size : list):
          
          self.title = title
          self.case = 0
          
          self.button = Button("resize", pos , [size[0] , 50] , self.title , target_arguments=self)
          
          for n in range(0 , 3):
               self.button.textures[n].fill([100 , 100 , 100])
          
          self.button.target = events.extend
          
          self.unpackaged_case_rect = Rect([pos[0] , pos[1]+self.button.rect.height] , [size[0] , size[1]])
          self.unpackaged_texture = pygame.Surface(self.unpackaged_case_rect.size)
          
          self.unpackaged_texture.fill([80 , 80 , 80])
          
          self.components = {}
     
     def load(self):
          pass
     
     def events(self , events : list[pygame.event.Event] , offset_detection=[0,0]):
          
          self.button.events(events=events , button_zone_offset=[offset_detection[0]+self.button.rect.x , offset_detection[1]+self.button.rect.y])
          
          if not self.case:
               for component in self.components.values():
                    
                    try:
                         component.events(events , [offset_detection[0] , offset_detection[1]+self.button.rect.height])
                    except:
                         pass
               
     
     def display(self , screen : pygame.Surface):
          
          if self.case:
               self.button.display(screen)
          else:
               self.button.display(screen)
               final_surface = self.unpackaged_texture.copy()  
               for component in self.components.values():
                    component.display(final_surface)
               
               screen.blit(final_surface , [self.unpackaged_case_rect.x , self.unpackaged_case_rect.y])
               # screen.blit(self.unpackaged_texture , [self.unpackaged_case_rect.x , self.unpackaged_case_rect.y])
               
   
class Basic_image_processing_package(Package):
     
     def __init__(self , pos : list, size : list , app_reference):
          
          super().__init__("Image processing" , pos , size)
          self.app_reference = app_reference
     
     def load(self):
          self.components["entry_img1"] = Entry("entry_img1" , [10 , 10] , [200 , 20])
          self.components["button_render"] = Button("button_render" , [220 , 10],[70 , 20],"render",target_arguments=self.app_reference)
          self.components["button_render"].target = events.load_image
          
          self.components["button_SymHori"] = Button("button_SymHori" , [10,40] , [280 , 30] , "Symétrie Horizontale" , target_arguments=self.app_reference)
          self.components["button_SymHori"].target = events.sym_hori
          
          self.components["button_SymVert"] = Button("button_SymVert" , [10,80] , [280 , 30] , "Symétrie Verticale" , target_arguments=self.app_reference)
          self.components["button_SymVert"].target = events.sym_vert

          self.components["button_rot180"] = Button("button_rot180" , [155,120] , [135 , 30] , "Rot. à 180°" , target_arguments=self.app_reference)
          self.components["button_rot180"].target = events.rot_180
          
          self.components["button_rot90"] = Button("button_rot90" , [10,120] , [135 , 30] , "Rot. à 90°" , target_arguments=self.app_reference)
          self.components["button_rot90"].target = events.rot_90
          
          self.components["button_convPGM"] = Button("button_convPGM" , [155,160] , [135 , 30] , "To PGM file" , target_arguments=self.app_reference)
          self.components["button_convPGM"].target = events.pgm_conv
          
          self.components["button_convPBM"] = Button("button_convPBM" , [10,160] , [135 , 30] , "To PBM file°" , target_arguments=self.app_reference)
          self.components["button_convPBM"].target = events.pbm_conv          
    