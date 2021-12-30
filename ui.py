import pygame
import events
import pyperclip
import os
import support

from pygame.locals import *

class Label():
     
     def __init__(self , pos : tuple , font_size : int , string_parameter):
          
          """
          string_parameter is a dictionnary with all parameters of the string
          Required key : stringValue
          """
          
          self.pos = pos
          self.stringValue = string_parameter["stringValue"]
          self.color = string_parameter["color"] if "color" in string_parameter else [0,0,0]
          
          self.font = pygame.font.Font("./fonts/pt_sans/PtSans-Regular.ttf", font_size )
     
     def event_handler(self , event):
          pass
     
     def change_font(self , font_size : int):
          self.font = pygame.font.Font("./fonts/pt_sans/PtSans-Regular.ttf", font_size )
     
     def display(self , surface):
          
          surface.blit(self.font.render(self.stringValue , True , self.color) , self.pos)


class Entry:
     
     def __init__(self , name : str , pos : tuple , size : tuple , target_arguments=None):
          
          self.name = name
          self.rect = Rect(pos , size)
          self.texture = pygame.Surface(size)
          self.texture.fill([160 , 160 , 160])
          self.stringValue = ""
          self.writing = False
          self.cursor = 0
          self.cursor_displayed = True
          self.target_arguments = target_arguments
          
          self.default_text = "Enter text"
          self.max_lenght = 200
          self.extra_string = ""
          
          self.font = pygame.font.Font("./fonts/pt_sans/PtSans-Regular.ttf", 14 )
          
          self.key_pressed = None
          self.timing = 0
          self.interval = [150 , 8 , False]
     
     def event_handler(self , event : pygame.event.Event , entry_zone_offset=[0,0]):
          
          if self.writing and self.key_pressed != None:
               self.timing += 1
               if not self.interval[2]:
                    if (self.timing % self.interval[0]) == 0:
                         self.timing = 0
                         self.interval[2] = True
               elif self.interval[2] and (self.timing % self.interval[1]) == 0:
                    self.timing = 0
                    
                    if self.key_pressed[0] == (K_BACKSPACE or K_DELETE):
                         self.stringValue = self.stringValue[:self.cursor-1]+self.stringValue[self.cursor:] if not self.cursor <= 0 else self.stringValue
                         self.cursor -= 1
                    
                    if self.key_pressed[1] in "abcdefghijklmnopqrstuvwxyz":
                         self.stringValue = self.stringValue[:self.cursor] + self.key_pressed[1] + self.stringValue[self.cursor:]
                         self.cursor += 1
                         
          
          if event.type == MOUSEBUTTONDOWN:
               if self.rect.x + entry_zone_offset[0] < event.pos[0] < self.rect.right + entry_zone_offset[0] and self.rect.y + entry_zone_offset[1] < event.pos[1] < self.rect.bottom + entry_zone_offset[1]:
                    self.writing = True
               else:
                    self.writing = False
          
          elif event.type == KEYDOWN and self.writing == True:
               self.key_pressed = (event.key , event.unicode)
               if event.key == (K_BACKSPACE or K_DELETE):
                    self.stringValue = self.stringValue[:self.cursor-1]+self.stringValue[self.cursor:] if not self.cursor <= 0 else self.stringValue
                    self.cursor -= 1
               elif event.key == K_RETURN:
                    self.writing = False
               elif (event.key == K_v and pygame.key.get_mods() & KMOD_CTRL):
                    pasted = pyperclip.paste()
                    self.stringValue = self.stringValue[:self.cursor]+pasted+self.stringValue[self.cursor:]
                    self.cursor += len(pasted)
               elif event.key == K_RIGHT:
                    self.cursor += 1
               elif event.key == K_LEFT:
                    self.cursor -= 1
               elif event.unicode in " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/\\-_.éàèù" and event.unicode != "" and len(self.stringValue) < self.max_lenght:
                    self.stringValue = self.stringValue[:self.cursor] + event.unicode + self.stringValue[self.cursor:]
                    self.cursor += 1
          
          elif event.type == KEYUP:
               self.key_pressed = None
               self.interval[2] = False
               
          if self.cursor > len(self.stringValue):
                    self.cursor -= 1
          elif 0 > self.cursor:
               self.cursor += 1
     
     def display(self , screen):
          
          final_surf = self.texture.copy()
          text_offset = (self.font.size(self.stringValue[:self.cursor]+self.extra_string)[0] + 1 - self.rect.width) if self.font.size(self.stringValue[:self.cursor]+self.extra_string)[0] > self.rect.width else 0
          
          if self.stringValue != "":
               pygame.draw.line(final_surf, [0,0,0], (self.font.size(self.stringValue[:self.cursor])[0]  + 1 - text_offset , self.rect.height // 2 - self.font.size(self.stringValue)[1] // 2), (self.font.size(self.stringValue[:self.cursor])[0] + 1 - text_offset , self.rect.height // 2 + self.font.size(self.stringValue)[1] // 2), 2) if self.writing else None
               final_surf.blit(self.font.render(self.stringValue+self.extra_string , True , [0,0,0]) , [1 - text_offset , self.rect.height // 2 - self.font.size(self.stringValue)[1] // 2])
          else:
               text_size = self.font.size(self.default_text)
               final_surf.blit(self.font.render(self.default_text , True , [0,0,0]) , [self.rect.width // 2 - text_size[0] // 2 , self.rect.height // 2 - text_size[1] // 2])
          screen.blit(final_surf , [self.rect.x , self.rect.y])

class Button():
     
     def __init__(self, pos : tuple , size : tuple , stringParameter : dict , target_arguments=None):
          
          self.rect = Rect(pos , size)
          self.textures = [pygame.Surface(self.rect.size),pygame.Surface(self.rect.size),pygame.Surface(self.rect.size)]
          
          self.textures[2].fill([100 , 100 , 100])
          self.textures[1].fill([230 , 230 , 230])
          self.textures[0].fill([150 , 150 , 150])
          
          self.target = None
          self.font = pygame.font.Font("./fonts/Readex_Pro/static/ReadexPro-Medium.ttf", 14)
          
          self.align_center = stringParameter["align center"] if "align center" in stringParameter else False
          self.padding_left = stringParameter["padding left"] if "padding left" in stringParameter else 0
          self.stringValue = stringParameter["stringvalue"]
          self.case = 0
          self.target_arguments = target_arguments
          
          self.hover_timer = 0
          self.event_time = 20
          self.display_hc = False
          self.hover_content = ""
          
     def event_handler(self , event : pygame.event.Event , button_zone_offset=[0,0]):
               
          if event.type == MOUSEBUTTONDOWN and event.button == 1:
               if self.rect.x + button_zone_offset[0] < event.pos[0] < self.rect.right + button_zone_offset[0] and self.rect.y + button_zone_offset[1] < event.pos[1] < self.rect.bottom + button_zone_offset[1]:
                    if self.target_arguments != None and self.target != None:
                         self.target(self.target_arguments)
                    elif self.target != None:
                         self.target()
                    self.case = 2
          elif event.type == MOUSEBUTTONUP and event.button == 1:
               if self.rect.x + button_zone_offset[0] < event.pos[0] < self.rect.right + button_zone_offset[0] and self.rect.y + button_zone_offset[1] < event.pos[1] < self.rect.bottom + button_zone_offset[1]:
                    self.case = 1
          elif event.type == MOUSEMOTION:
               if self.rect.x + button_zone_offset[0] < event.pos[0] < self.rect.right + button_zone_offset[0] and self.rect.y + button_zone_offset[1] < event.pos[1] < self.rect.bottom + button_zone_offset[1]:
                    self.case = 1
               else:
                    self.case = 0
                    
     
     def display(self , screen):
          
          final_texture = self.textures[self.case].copy()
          if self.align_center:
               final_texture.blit(self.font.render(self.stringValue , True , [0,0,0]) , [self.rect.width // 2 - self.font.size(self.stringValue)[0] // 2 , self.rect.height // 2 - self.font.size(self.stringValue)[1] // 2])
          else:
               final_texture.blit(self.font.render(self.stringValue , True , [0,0,0]) , [self.padding_left , self.rect.height // 2 - self.font.size(self.stringValue)[1] // 2])
          screen.blit(final_texture , [self.rect.x , self.rect.y])

class Image_selector(Button):
     
     def __init__(self, pos : tuple , size : tuple , stringValue : str , value):
          super().__init__(pos , size , stringValue , None)
          
          self.selected = False
          self.value = value
          
          self.delete_button = Button([self.rect.width - self.rect.height , 0],[self.rect.height]*2 , {"stringvalue":""} , self)
          self.delete_button.target = events.remove_ffl
          
          self.delete_button.textures = [pygame.Surface([self.rect.height]*2 , SRCALPHA)]*3
          self.delete_button.textures[0].fill([200 , 200 , 200 , 20])
          
          self.save_button = Button([self.rect.width - self.rect.height*2 , 0],[self.rect.height]*2 , {"stringvalue":""})
          self.save_button.target = self.value.save
          
          self.save_button.textures = [pygame.Surface([self.rect.height]*2 , SRCALPHA)]*3
          self.save_button.textures[0].fill([200 , 200 , 200 , 20])
          
          self.display_sb = False
     
     def event_handler(self, event: pygame.event.Event, button_zone_offset=[0, 0]):
          
          if event.type == MOUSEBUTTONDOWN and event.button == 1:
               if self.rect.x + button_zone_offset[0] < event.pos[0] < self.rect.right + button_zone_offset[0] and self.rect.y + button_zone_offset[1] < event.pos[1] < self.rect.bottom + button_zone_offset[1]:
                    self.target(self.value)
                    if self.display_sb:
                         self.delete_button.event_handler(event , [button_zone_offset[0]+self.rect.x , button_zone_offset[1]+self.rect.y])
                         self.save_button.event_handler(event , [button_zone_offset[0]+self.rect.x , button_zone_offset[1]+self.rect.y])
                    self.selected = True
               else:
                    self.selected = False
                    self.case = 0
               
               
                    
          if event.type == MOUSEMOTION:
               if self.rect.x + button_zone_offset[0] < event.pos[0] < self.rect.right + button_zone_offset[0] and self.rect.y + button_zone_offset[1] < event.pos[1] < self.rect.bottom + button_zone_offset[1]:
                    
                    self.display_sb = True
               else:
                    self.display_sb = False
                    
          
          if self.selected:
               self.case = 2
          else:
               self.case = 0
     
     def display(self , screen):
          
          final_texture = self.textures[self.case].copy()
          if self.align_center:
               final_texture.blit(self.font.render(self.stringValue , True , [0,0,0]) , [self.rect.width // 2 - self.font.size(self.stringValue)[0] // 2 , self.rect.height // 2 - self.font.size(self.stringValue)[1] // 2])
          else:
               final_texture.blit(self.font.render(self.stringValue , True , [0,0,0]) , [self.padding_left , self.rect.height // 2 - self.font.size(self.stringValue)[1] // 2])
          
          if self.display_sb:
               self.delete_button.display(final_texture)
               self.save_button.display(final_texture)
          
          screen.blit(final_texture , [self.rect.x , self.rect.y])
     
          
class Image():
     
     def __init__(self, pos : tuple):
     
          self.name = ""
          self.path = ""
          self.pos = pos
          self.image_loaded = False
          self.image_data = {}
          
          self.image_data_backup = []
     
     def load(self , path):
          
          self.path = path
          filepath , file_extension = os.path.splitext(self.path)
          self.name = os.path.basename(self.path)
          self.image_data = {"meta" : {"titre": filepath,
                         "extension": file_extension,
                         "col" : None,
                         "lig" : None,
                         "mod" : "",
                         "readable" : True},
               "pix" : []}
          
          if file_extension == ".pgm":
               self.image_data = support.readPGM(self.path,self.image_data)
          elif file_extension == ".pbm":
               self.image_data = support.readPBM(self.path,self.image_data)
          elif file_extension == ".ppm":
               self.image_data = support.readPPM(self.path,self.image_data)
          else:
               self.texture = pygame.image.load(self.path)
               self.texture.convert_alpha()
               self.image_data["readable"] = False
               
               self.rect = self.texture.get_rect()
               self.rect.x , self.rect.y = self.pos[0] , self.pos[1]
               
               self.image_loaded = True
               
               return
          
          self.texture = pygame.Surface([self.image_data["meta"]["col"] , self.image_data["meta"]["lig"]])
          
          for y in range(self.image_data["meta"]["lig"]):
               
               for x in range(self.image_data["meta"]["col"]):
                    
                    self.texture.set_at([x , y] , self.image_data["pix"][y][x])
          
          self.rect = self.texture.get_rect()
          self.rect.x , self.rect.y = self.pos[0] , self.pos[1]
          
          self.image_loaded = True
     
     def load_by_data(self , image_data : dict , save=True):
          
          if save:
               self.image_data_backup.append(self.image_data)
               
               if len(self.image_data_backup) == 3:
                    print(self.image_data_backup)
                    self.image_data_backup.pop(0)
          
          self.image_data = image_data
          
          self.texture = pygame.Surface([self.image_data["meta"]["col"] , self.image_data["meta"]["lig"]])
          
          for y in range(self.image_data["meta"]["lig"]):
               
               for x in range(self.image_data["meta"]["col"]):
                    self.texture.set_at([x , y] , self.image_data["pix"][y][x])
                         
          
          self.rect = self.texture.get_rect()
          self.rect.x , self.rect.y = self.pos[0] , self.pos[1]
          
          self.image_loaded = True
     
     def save(self):
          
          col = self.image_data["meta"]["col"]
          lig = self.image_data["meta"]["lig"]
          img_format = {".pbm":'P1', ".pgm":'P2', ".ppm":'P3'}[self.image_data["meta"]["extension"]]
          pix = self.image_data["pix"]
          nom = self.image_data["meta"]["titre"] + "_modifie" + self.image_data["meta"]["extension"]

          with open(nom, 'w') as f :
               f.write(img_format + '\n' + str(col) + '\n' + str(lig) + '\n')

               if img_format in ["P2", "P3"]:
                    f.write('255\n')

               if img_format == "P1":
                    for y in range(lig):
                         for x in range(col):
                              val = pix[y][x][0]
                              if val == 0:
                                   f.write(' 1')
                              else:
                                   f.write(' 0')
                         f.write('\n')

               if img_format == "P2":
                    for y in range(lig):
                         for x in range(col):
                              val = str(pix[y][x][0])
                              f.write(' '*(4-len(val))+val)
                         f.write('\n')

               elif img_format == "P3":
                    for y in range(lig):
                         for x in range(col):
                              for i in range(3):
                                   val = str(pix[y][x][i])
                                   f.write(' '*(4-len(val))+val)
                         f.write('\n')
               f.close()
          
     
     def display(self , surface : pygame.Surface , centered=False):
          
          try:
               if not centered:
                    surface.blit(self.texture , [self.rect.x, self.rect.y])
               else:
                    surface.blit(self.texture , [surface.get_rect().width // 2 - self.rect.width // 2, surface.get_rect().height // 2 - self.rect.height // 2])
          except:
               pass

class Img_displayer():
     
     def __init__(self, pos : list , size : list):
          
          self.rect = Rect(pos , size)
          
          self.surface = pygame.Surface(self.rect.size)
          
          self.image = Image([0,0])
          self.zoom = 3
          self.zooms = [0.25 , 0.5 , 0.75 , 1 , 1.25 , 1.5 , 1.75 , 2 , 2.5 , 3 , 3.5 , 4 , 4.5 , 5 , 7.5 , 10 , 15 , 20]
     
     def event_handler(self , event : pygame.event.Event , offset_detection=[0,0]):
               
          if event.type == MOUSEBUTTONDOWN:
               
               if event.button == 4 and offset_detection[0] < event.pos[0] < self.rect.right + offset_detection[0] and offset_detection[1] < event.pos[1] < self.rect.right + offset_detection[1]:
                    self.zoom += 1
                    if self.zoom > 17:
                         self.zoom = 17
               
               if event.button == 5 and offset_detection[0] < event.pos[0] < self.rect.right + offset_detection[0] and offset_detection[1] < event.pos[1] < self.rect.right + offset_detection[1]:
                    self.zoom -= 1 
                    if self.zoom < 0:
                         self.zoom = 0
     
     def resize(self):
          
          final_zoom = 3
          
          if self.image.rect.width > self.rect.width:
               for z in range(3 , 0 , -1):
                    final_zoom -= 1
                    if self.image.rect.width * self.zooms[final_zoom] < self.rect.width:
                         self.zoom = final_zoom
                         return
          elif self.image.rect.height > self.rect.height:
               
               for z in range(3 , 0 , -1):
                    final_zoom -= 1
                    if self.image.rect.height * self.zooms[final_zoom] < self.rect.height:
                         self.zoom = final_zoom
                         return
          else:
               for z in range(0 , 14 , 1):
                    final_zoom += 1
                    if round((self.image.rect.width * self.zooms[final_zoom]) / self.rect.width , 2) > 0.7:
                         self.zoom = final_zoom
                         return
          
          self.zoom = final_zoom
                    
               
     
     def display(self , surface : pygame.Surface):
          
          final_surface = self.surface.copy()
          if self.image.image_loaded:
               image = pygame.transform.scale(self.image.texture, [self.image.rect.width*self.zooms[self.zoom] , self.image.rect.height*self.zooms[self.zoom]])
               final_surface.blit(image , [self.rect.width // 2 - image.get_rect().width // 2 , self.rect.height // 2 - image.get_rect().height // 2 ])
          surface.blit(final_surface , [self.rect.x , self.rect.y])      