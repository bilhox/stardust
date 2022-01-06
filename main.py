import pygame
import sys
import events
import filters

from ui import *
from pygame.locals import *
from panel import *
from window import *

class App():
     
     def __init__(self):
          
          self.name = "Stardust"
          self.version = "V0.1.9.2"
          
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
          
          self.panels["settings bar"].components["button_addFile"] = Button("addFile",[0,0],[80 , 20],{"stringvalue":"open file","align center":True},self.windows["File manager"])
          self.panels["settings bar"].components["button_addFile"].target = events.open_window
          
          #Tool panel components
          self.panels["Tool panel"] = UI_panel_with_selectors([0 , 425],[900 , 175])
          
          self.panels["Tool panel"].create_panel("main tools")
          self.panels["Tool panel"].create_panel("filters")
          
          self.panels["Tool panel"].set_panel("main tools")
          
          # main tools preparation
          main_tools = self.panels["Tool panel"].panels["main tools"]
          main_tools.components["button_SymHori"] = Button("SymHori",[10, 5] , [150 , 40] , {"stringvalue":"Hor. sym","padding left":60,"color":[255 , 255 , 255]})
          main_tools.components["button_SymHori"].target = events.sym_hori
          
          main_tools.components["button_SymVert"] = Button("SymVert",[10,50] , [150 , 40] , {"stringvalue":"Vert. sym","padding left":60,"color":[255 , 255 , 255]})
          main_tools.components["button_SymVert"].target = events.sym_vert

          main_tools.components["button_rot180"] = Button("rot180",[165,50] , [150 , 40] , {"stringvalue":"Rot. 180°","padding left":60,"color":[255 , 255 , 255]})
          main_tools.components["button_rot180"].target = events.rot_180
          
          main_tools.components["button_rot90"] = Button("rot90",[165,5] , [150 , 40] , {"stringvalue":"Rot. 90°","padding left":60,"color":[255 , 255 , 255]})
          main_tools.components["button_rot90"].target = events.rot_90
          
          main_tools.components["button_convPGM"] = Button("convPGM",[165,95] , [150 , 40] , {"stringvalue":"To PGM","padding left":60,"color":[255 , 255 , 255]})
          main_tools.components["button_convPGM"].target = events.pgm_conv
          
          main_tools.components["button_convPBM"] = Button("convPBM",[350,95] , [150 , 40] , {"stringvalue":"To PBM :","padding left":60,"color":[255 , 255 , 255]})
          main_tools.components["button_convPBM"].target = events.pbm_conv  
          
          main_tools.components["entry_intConvPBM"] =  Entry("entry_intConvPBM", [505 , 95] , [75 , 40] , [255 , 255 , 255])
          main_tools.components["entry_intConvPBM"].default_text = "Int - %"   
          main_tools.components["entry_intConvPBM"].max_lenght = 3
          main_tools.components["entry_intConvPBM"].extra_string = "%" 
          
          main_tools.components["button_brightness"] = Button("brightness",[350,5] , [150 , 40] , {"stringvalue":"brightness :","padding left":60,"color":[255 , 255 , 255]})
          main_tools.components["button_brightness"].target = events.luminosity
          
          main_tools.components["entry_luminance"] =  Entry("entry_luminance", [505 , 5] , [75 , 40] , [255 , 255 , 255])
          main_tools.components["entry_luminance"].default_text = "Lum - %"   
          main_tools.components["entry_luminance"].max_lenght = 3
          main_tools.components["entry_luminance"].extra_string = "%" 
          
          main_tools.components["button_saturation"] = Button("saturation",[350,50] , [150 , 40] , {"stringvalue":"saturate :","padding left":60,"color":[255 , 255 , 255]})
          main_tools.components["button_saturation"].target = events.saturation
          
          main_tools.components["entry_saturation"] =  Entry("entry_saturation", [505 , 50] , [75 , 40] , [255 , 255 , 255])
          main_tools.components["entry_saturation"].default_text = "sat - %"   
          main_tools.components["entry_saturation"].max_lenght = 3
          main_tools.components["entry_saturation"].extra_string = "%" 
          
          main_tools.components["button_rotation"] = Button("rotation",[610,5] , [150 , 40] , {"stringvalue":"rotate :","padding left":60,"color":[255 , 255 , 255]})
          main_tools.components["button_rotation"].target = events.rotation
          
          main_tools.components["entry_rotation"] =  Entry("entry_rotation", [765 , 5] , [75 , 40] , [255 , 255 , 255])
          main_tools.components["entry_rotation"].default_text = "rot - °"   
          main_tools.components["entry_rotation"].max_lenght = 3
          main_tools.components["entry_rotation"].extra_string = "°" 
          
          main_tools.components["button_resize"] = Button("resize",[610,50] , [150 , 40] , {"stringvalue":"resize :","padding left":60,"color":[255 , 255 , 255]})
          main_tools.components["button_resize"].target = events.resize_image
          
          main_tools.components["entry_xSize"] =  Entry("entry_xSize", [765 , 50] , [75 , 40] , [255 , 255 , 255])
          main_tools.components["entry_xSize"].default_text = "X - pixel"   
          main_tools.components["entry_xSize"].max_lenght = 4
          main_tools.components["entry_xSize"].extra_string = "px" 
          
          main_tools.components["entry_ySize"] =  Entry("entry_ySize", [765 , 95] , [75 , 40] , [255 , 255 , 255])
          main_tools.components["entry_ySize"].default_text = "Y - pixel"   
          main_tools.components["entry_ySize"].max_lenght = 4
          main_tools.components["entry_ySize"].extra_string = "px" 
     
          main_tools.components["button_undo"] = Button("undo",[860,105] , [40 , 40] , {"stringvalue":"","align center":True,"color":[255 , 255 , 255]})
          main_tools.components["button_undo"].target = events.undo
          
          #filters preparation
          filter_tools = self.panels["Tool panel"].panels["filters"]
          
          filter_tools.components["filter selector"] = Filter_selector([0,0],[900 , filter_tools.rect.height])
          filter_selector = filter_tools.components["filter selector"]
          filter_selector.color = [18, 12, 54]
          
          filter_selector.add_filter(filters.red , "Red filter")
          filter_selector.add_filter(filters.contour , "contours")

     
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
          
          if self.current_window != None:
               self.current_window.update()
          else:
               self.panels["Tool panel"].panels["filters"].components["filter selector"].update()
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
               self.current_window.display(self.screen)

def main():
     app = App()
     events.app = app
     app.Start()
     app.load_textures()

     while True:
          app.Update()

if __name__ == "__main__":
     main()
               
               