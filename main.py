import pygame
import sys
import events

from ui import *
from pygame.locals import *
from panel import *
from window import *

class App():
     
     def __init__(self):
          
          self.name = "Stardust"
          self.version = "V0.1.6"
          
          self.window_size = [900 , 600]
          
          self.panels = {}
          self.windows = {}
          self.ui = {}
          
          self.screen = pygame.display.set_mode(self.window_size)
          pygame.display.set_caption(self.name + " - " + self.version)
          
          icon = pygame.image.load("./imgs/logo.png")
          icon.convert_alpha()
          pygame.display.set_icon(icon)
          
          self.is_window_open = False
          self.current_window = None
     
     def Start(self):
          
          pygame.font.init()
          
          self.screen.fill([90 , 90 , 90])
          
          self.panels["Img displayer"] = Img_displayer_panel([300 , 20] , [600 , 400])
          self.windows["File manager"] = File_manager()
          self.panels["Tool panel"] = UI_panel_with_selectors([0 , 425],[900 , 175])
          
          self.panels["File list"] = Image_list([0 , 20],[300 , 400])
          self.panels["File list"].color = [18, 12, 54]
          
          self.panels["settings bar"] = Settings_bar([0,0],[900 , 20])
          self.panels["settings bar"].texture.fill([242, 160, 73])
          
          self.panels["settings bar"].components["button_addFile"] = Button( [0,0],[80 , 20],{"stringvalue":"open file","align center":True},self.windows["File manager"])
          self.panels["settings bar"].components["button_addFile"].target = events.open_window
          
          self.panels["settings bar"].load_textures()
          self.panels["Tool panel"].load_textures()
          self.windows["File manager"].load_textures()
     
     def events(self):
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
                    
               if(not self.is_window_open):
                    for panel in self.panels.values():
                         panel.event_handler(event)
                         
                    for ui in self.ui.values():
                         ui.event_handler(event)
               else:
                    self.current_window.event_handler(event)
     
     def Update(self):
          
          self.events()
          
          self.panels["File list"].update()
          
          if self.current_window != None:
               self.current_window.update()
          
          self.Display()
          pygame.display.flip()
     
     def Display(self):
          
          if not self.is_window_open:
               self.screen.fill([245, 174, 39])
               
               for panel in self.panels.values():
                    panel.display(self.screen)
               
               for ui in self.ui.values():
                    ui.display(self.screen)
          else:
               self.current_window.display(self.screen)

def main():
     app = App()
     events.app = app
     app.Start()

     while True:
          app.Update()

if __name__ == "__main__":
     main()
               
               