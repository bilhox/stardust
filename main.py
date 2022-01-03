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
          self.version = "V0.1.6.5"
          
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
          
          self.panels["File list"] = Selector_list([0 , 20],[300 , 400])
          self.panels["File list"].color = [18, 12, 54]
          
          self.panels["settings bar"] = Settings_bar([0,0],[900 , 20])
          self.panels["settings bar"].texture.fill([242, 160, 73])
          
          self.panels["settings bar"].components["button_addFile"] = Button( [0,0],[80 , 20],{"stringvalue":"open file","align center":True},self.windows["File manager"])
          self.panels["settings bar"].components["button_addFile"].target = events.open_window
          
          #Tool panel components
          self.panels["Tool panel"] = UI_panel_with_selectors([0 , 425],[900 , 175])
          
          self.panels["Tool panel"].create_panel("main tools")
          self.panels["Tool panel"].create_panel("filters")
          
          self.panels["Tool panel"].set_panel("main tools")
          
          # main tools preparation
          main_tools = self.panels["Tool panel"].panels["main tools"]
          main_tools.components["button_SymHori"] = Button([10, 5] , [200 , 30] , {"stringvalue":"Horizontal symmetry","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_SymHori"].target = events.sym_hori
          
          main_tools.components["button_SymVert"] = Button([10,40] , [200 , 30] , {"stringvalue":"Vertical symmetry","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_SymVert"].target = events.sym_vert

          main_tools.components["button_rot180"] = Button([10,75] , [200 , 30] , {"stringvalue":"Rotation 180°","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_rot180"].target = events.rot_180
          
          main_tools.components["button_rot90"] = Button([10,110] , [200 , 30] , {"stringvalue":"Rotation 90°","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_rot90"].target = events.rot_90
          
          main_tools.components["button_convPGM"] = Button([240,5] , [120 , 30] , {"stringvalue":"To PGM","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_convPGM"].target = events.pgm_conv
          
          main_tools.components["button_convPBM"] = Button([240,40] , [120 , 30] , {"stringvalue":"To PBM :","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_convPBM"].target = events.pbm_conv  
          
          main_tools.components["entry_intConvPBM"] =  Entry("entry_intConvPBM", [370 , 40] , [120 , 30] , [255 , 255 , 255])
          main_tools.components["entry_intConvPBM"].default_text = "Intensity - %"   
          main_tools.components["entry_intConvPBM"].max_lenght = 3
          main_tools.components["entry_intConvPBM"].extra_string = "%" 
          
          main_tools.components["button_lum"] = Button([240,75] , [120 , 30] , {"stringvalue":"brightness :","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_lum"].target = events.luminosity
          
          main_tools.components["entry_luminance"] =  Entry("entry_luminance", [370 , 75] , [120 , 30] , [255 , 255 , 255])
          main_tools.components["entry_luminance"].default_text = "Luminance - %"   
          main_tools.components["entry_luminance"].max_lenght = 3
          main_tools.components["entry_luminance"].extra_string = "%" 
          
          main_tools.components["button_saturation"] = Button([240,110] , [120 , 30] , {"stringvalue":"saturate :","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_saturation"].target = events.saturation
          
          main_tools.components["entry_saturation"] =  Entry("entry_saturation", [370 , 110] , [120 , 30] , [255 , 255 , 255])
          main_tools.components["entry_saturation"].default_text = "saturation - %"   
          main_tools.components["entry_saturation"].max_lenght = 3
          main_tools.components["entry_saturation"].extra_string = "%" 
          
          main_tools.components["button_rotation"] = Button([520,5] , [120 , 30] , {"stringvalue":"rotate :","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_rotation"].target = events.rotation
          
          main_tools.components["entry_rotation"] =  Entry("entry_rotation", [650 , 5] , [120 , 30] , [255 , 255 , 255])
          main_tools.components["entry_rotation"].default_text = "rotation - °"   
          main_tools.components["entry_rotation"].max_lenght = 3
          main_tools.components["entry_rotation"].extra_string = "°" 
          
          main_tools.components["button_resize"] = Button([520,50] , [120 , 30] , {"stringvalue":"resize :","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_resize"].target = events.resize_image
          
          main_tools.components["entry_xSize"] =  Entry("entry_xSize", [650 , 50] , [120 , 30] , [255 , 255 , 255])
          main_tools.components["entry_xSize"].default_text = "X - pixel"   
          main_tools.components["entry_xSize"].max_lenght = 4
          main_tools.components["entry_xSize"].extra_string = "px" 
          
          main_tools.components["entry_ySize"] =  Entry("entry_ySize", [650 , 85] , [120 , 30] , [255 , 255 , 255])
          main_tools.components["entry_ySize"].default_text = "Y - pixel"   
          main_tools.components["entry_ySize"].max_lenght = 4
          main_tools.components["entry_ySize"].extra_string = "px" 
          
          main_tools.components["button_undo"] = Button([850,0] , [50 , 30] , {"stringvalue":"undo","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_undo"].target = events.undo
          
          #filters preparation
          filter_tools = self.panels["Tool panel"].panels["filters"]
          
          filter_tools.components["filter selector"] = Selector_list([0,0],[900 , filter_tools.rect.height],True)
          filter_tools.components["filter selector"].color = [18, 12, 54]
     
     def load_textures(self):
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
               pygame.draw.line(self.screen, [255 , 0 , 0], [180 , 165], [180 , 165], 2)

def main():
     app = App()
     events.app = app
     app.Start()
     app.load_textures()

     while True:
          app.Update()

if __name__ == "__main__":
     main()
               
               