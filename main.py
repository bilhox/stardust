import pygame
import sys
import events
from components import *
from pygame.locals import *
from extensions import *

class App():
     
     def __init__(self , window_size : tuple):
          
          self.name = "Stardust"
          self.version = "V0.1.3"
          
          self.window_size = window_size
          
          self.ui_components = {}
          self.packages = {}
          self.canva_components = {}
          self.surface = {}
          
          self.tool_surface = pygame.Surface([int(self.window_size[0]*0.3) , int(self.window_size[1]*0.95)])
          self.tool_surface_rect = self.tool_surface.get_rect()
          
          self.canva_surface = pygame.Surface([int(self.window_size[0]*0.7) , int(self.window_size[1]*0.95)])
          self.canva_surface_rect = self.canva_surface.get_rect()
          
          self.settings_surface = pygame.Surface([self.window_size[0] , int(self.window_size[1]*0.05)])
          self.settings_surface_rect = self.settings_surface.get_rect()
          
          self.screen = pygame.display.set_mode(self.window_size)
          pygame.display.set_caption(self.name + " - " + self.version)
          
          icon = pygame.image.load("./imgs/logo.png")
          icon.convert_alpha()
          pygame.display.set_icon(icon)
     
     def Start(self):
          
          pygame.font.init()
          
          self.screen.fill([90 , 90 , 90])
          
          
          self.tool_surface_rect.x , self.tool_surface_rect.y = [0 , self.window_size[1] - self.tool_surface_rect.height]
          self.canva_surface_rect.x , self.canva_surface_rect.y = [self.tool_surface_rect.right , self.window_size[1] - self.canva_surface_rect.height]
          
          self.canva_components["toile"] = Canva("toile" , [0,0] , self.canva_surface_rect.size)
          self.canva_components["toile"].image = Image("image" , "" , [0,0])
          
          self.packages["traitement"] = Basic_image_processing_package([0,0],[self.tool_surface_rect.width , 200] , self)
          
          self.packages["traitement"].load()
          
          self.ui_components["button_reset_img"] = Button("button_resetImg" , [self.tool_surface_rect.width // 2 - 100 , self.tool_surface_rect.height - 40] , [200 , 30] , "reset" , target_arguments=self)
          self.ui_components["button_reset_img"].target = events.reset_image
          
          self.file_founded = False
          
     
     def events(self):
          events = []
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
               events.append(event)
          
          for package in self.packages.values():
               package.events(events , [self.tool_surface_rect.x , self.tool_surface_rect.y])
          
          for component in self.ui_components.values():
               component.events(events , [self.tool_surface_rect.x , self.tool_surface_rect.y])
          
          for canva_component in self.canva_components.values():
               canva_component.events(events , [self.canva_surface_rect.x , self.canva_surface_rect.y])
     
     def Update(self):
          
          self.events()
          self.Display()
          pygame.display.flip()
     
     def Display(self):
          
          self.tool_surface.fill([60 , 60 , 60])
          
          for package in self.packages.values():
               package.display(self.tool_surface)
          
          for component in self.ui_components.values():
               component.display(self.tool_surface)
          
          self.screen.blit(self.tool_surface , [0 , self.window_size[1] - self.tool_surface_rect.height])
          
          self.canva_surface.fill([30 , 30 , 30])
               
          for canva_component in self.canva_components.values():
               
               if isinstance(canva_component , Image):
                    canva_component.display(self.canva_surface , True)
               else:
                    canva_component.display(self.canva_surface)
               

          self.screen.blit(self.canva_surface , [self.tool_surface_rect.right , self.window_size[1] - self.canva_surface_rect.height])
          
          self.settings_surface.fill([54, 171, 104])
          
          self.screen.blit(self.settings_surface , [0,0])

def main():
     app = App([1000 , 650])
     app.Start()

     while True:
          app.Update()

if __name__ == "__main__":
     main()
               
               