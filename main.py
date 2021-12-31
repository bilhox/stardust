import pygame
import sys
import events
from ui import *
from pygame.locals import *
from panel import *

class App():
     
     def __init__(self):
          
          self.name = "Stardust"
          self.version = "V0.1.5.2"
          
          self.window_size = [900 , 600]
          
          self.panels = {}
          self.ui = {}
          
          self.screen = pygame.display.set_mode(self.window_size)
          pygame.display.set_caption(self.name + " - " + self.version)
          
          icon = pygame.image.load("./imgs/logo.png")
          icon.convert_alpha()
          pygame.display.set_icon(icon)
          
          self.is_window_open = False
     
     def Start(self):
          
          pygame.font.init()
          
          self.screen.fill([90 , 90 , 90])
          
          self.panels["Img displayer"] = Img_displayer_panel([300 , 40] , [600 , 380])
          self.panels["File manager"] = Window_panel([400 , 500])
          self.panels["Tool panel"] = UI_panel_with_selectors([0 , 425],[900 , 175])
          
          self.panels["File list"] = Image_list([0 , 40],[300 , 380])
          self.panels["File list"].color = [18, 12, 54]
          
          self.ui["label_of"] = Label([10 , 5] , 20 , {"stringValue":"Open file :"})
          
          self.ui["entry_img1"] = Entry("entry_img1" , [self.ui["label_of"].font.size(self.ui["label_of"].stringValue)[0] + 20 , 5] , [300 , 30])
          self.ui["entry_img1"].default_text = "Enter img path :"
          
          self.ui["button_addFile"] = Button( [self.ui["entry_img1"].rect.width + self.ui["entry_img1"].rect.x + 5 , 5],[40 , 30],{"stringvalue":"add","align center":True})
          self.ui["button_addFile"].target = events.add_file
     
     def events(self):
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
               
               for panel in self.panels.values():
                    
                    if not self.is_window_open:
                         panel.event_handler(event)
                    else:
                         if isinstance(panel , Window_panel):
                              panel.event_handler(event)
                         
               if not self.is_window_open:
                    for ui in self.ui.values():
                         ui.event_handler(event)
     
     def Update(self):
          
          self.events()
          
          self.panels["File list"].update()
          
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
               for panel in self.panels.values():
                    if isinstance(panel , Window_panel):
                         panel.display(self.screen)

def main():
     app = App()
     events.app = app
     app.Start()

     while True:
          app.Update()

if __name__ == "__main__":
     main()
               
               