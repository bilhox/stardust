import pygame
import sys
import events
from ui import *
from pygame.locals import *
from panel import *

class App():
     
     def __init__(self , window_size : tuple):
          
          self.name = "Stardust"
          self.version = "V0.1.4.2"
          
          self.window_size = window_size
          
          self.panels = {}
          self.ui = {}
          
          self.screen = pygame.display.set_mode(self.window_size)
          pygame.display.set_caption(self.name + " - " + self.version)
          
          icon = pygame.image.load("./imgs/logo.png")
          icon.convert_alpha()
          pygame.display.set_icon(icon)
     
     def Start(self):
          
          pygame.font.init()
          
          self.screen.fill([90 , 90 , 90])
          
          self.panels["Img displayer"] = Img_displayer_panel([300 , 40] , [600 , 380])
          self.panels["File list"] = File_list([0 , 40],[300 , 380])
          
          self.ui["label_of"] = Label([10 , 5] , 20 , {"stringValue":"Open file :"})
          
          self.ui["entry_img1"] = Entry("entry_img1" , [self.ui["label_of"].font.size(self.ui["label_of"].stringValue)[0] + 20 , 5] , [300 , 30])
          self.ui["entry_img1"].default_text = "Enter img path :"
          
          self.ui["button_addFile"] = Button( [self.ui["entry_img1"].rect.width + self.ui["entry_img1"].rect.x + 5 , 5],[40 , 30],{"stringvalue":"add","align center":True})
          self.ui["button_addFile"].target = events.add_file
          
          self.ui["button_SymHori"] = Button([10,430] , [200 , 30] , {"stringvalue":"Horizontal symmetry","align center":True})
          self.ui["button_SymHori"].target = events.sym_hori
          
          self.ui["button_SymVert"] = Button([10,470] , [200 , 30] , {"stringvalue":"Vertical symmetry","align center":True})
          self.ui["button_SymVert"].target = events.sym_vert

          self.ui["button_rot180"] = Button([50,510] , [120 , 30] , {"stringvalue":"Rot 180°","align center":True})
          self.ui["button_rot180"].target = events.rot_180
          
          self.ui["button_rot90"] = Button([50,550] , [120 , 30] , {"stringvalue":"Rot 90°","align center":True})
          self.ui["button_rot90"].target = events.rot_90
          
          self.ui["button_convPGM"] = Button([240,430] , [120 , 30] , {"stringvalue":"To PGM","align center":True})
          self.ui["button_convPGM"].target = events.pgm_conv
          
          self.ui["button_convPBM"] = Button([240,470] , [120 , 30] , {"stringvalue":"To PBM","align center":True})
          self.ui["button_convPBM"].target = events.pbm_conv  
          
          self.ui["entry_intConvPBM"] =  Entry("entry_intConvPBM", [370 , 470] , [120 , 30])
          self.ui["entry_intConvPBM"].default_text = "Intensity"   
          self.ui["entry_intConvPBM"].max_lenght = 3 
          
          self.ui["button_lum"] = Button([240,510] , [120 , 30] , {"stringvalue":"Brightness","align center":True})
          self.ui["button_lum"].target = events.luminosity
          
          self.ui["entry_luminance"] =  Entry("entry_luminance", [370 , 510] , [120 , 30])
          self.ui["entry_luminance"].default_text = "Luminance - %"   
          self.ui["entry_luminance"].max_lenght = 4
          self.ui["entry_luminance"].extra_string = "%" 
          
          self.ui["button_saturation"] = Button([240,550] , [120 , 30] , {"stringvalue":"Saturation","align center":True})
          self.ui["button_saturation"].target = events.saturation
          
          self.ui["entry_saturation"] =  Entry("entry_saturation", [370 , 550] , [120 , 30])
          self.ui["entry_saturation"].default_text = "saturation - %"   
          self.ui["entry_saturation"].max_lenght = 4
          self.ui["entry_saturation"].extra_string = "%" 
          
          # self.ui["button_rotation"] = Button([520,430] , [120 , 30] , {"stringvalue":"Rotate","align center":True})
          # self.ui["button_rotation"].target = events.rotation
          
          # self.ui["entry_rotation"] =  Entry("entry_rotation", [650 , 430] , [120 , 30])
          # self.ui["entry_rotation"].default_text = "rotation - °"   
          # self.ui["entry_rotation"].max_lenght = 4
          # self.ui["entry_rotation"].extra_string = "°" 
          
          self.ui["button_undo"] = Button([850,420] , [50 , 30] , {"stringvalue":"undo","align center":True})
          self.ui["button_undo"].target = events.undo
     
     def events(self):
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
               
               for panel in self.panels.values():
                    
                    panel.event_handler(event)
               
               for ui in self.ui.values():
                    ui.event_handler(event)
     
     def Update(self):
          
          self.events()
          
          self.panels["File list"].update()
          
          self.Display()
          pygame.display.flip()
     
     def Display(self):
          
          self.screen.fill([90,90,90])
          
          for panel in self.panels.values():
               panel.display(self.screen)
          
          for ui in self.ui.values():
               ui.display(self.screen)

def main():
     app = App([900 , 600])
     events.app = app
     app.Start()

     while True:
          app.Update()

if __name__ == "__main__":
     main()
               
               