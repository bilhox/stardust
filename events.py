import pygame
import traitement

from ui import *
from image import *
from window import *
from pygame.locals import *

app = None

def filter(filter_function):
     try:
          image_data = filter_function(app.panels["Img displayer"].image.image_data)
          app.panels["Img displayer"].image.load_by_data(image_data)
     except:
          pass

def open_window(window):
     
     filtre = pygame.Surface(app.screen.get_rect().size , SRCALPHA)
     filtre.fill([0, 0, 0 , 128])
     
     app.screen.blit(filtre , [0,0])
     
     window.start()
     window.opened = True
     app.is_window_open = True
     app.current_window = window

def close_window(window):
     
     window.opened = False
     app.is_window_open = False
     app.current_window = None


def undo():
     try:
          backup = app.panels["Img displayer"].image.image_data_backup.pop()
          app.panels["Img displayer"].image.load_by_data(backup , False)
     except:
          pass

def search_files():

     try:
          path = app.current_window.components["entry_folderPath"].stringValue
          file_list = os.listdir(path)
          image_list = []
          
          for file_path in file_list:
               if os.path.splitext(file_path)[1].lower() in [".png" , ".jpg" , ".ppm" , ".pbm" , ".pgm"]:
                    image_list.append(file_path)
          
          if len(app.current_window.components["FileList_fileFounded"].selectors) != 0:
               app.current_window.components["FileList_fileFounded"].selectors = []
          
          for file in image_list:
               height = len(app.current_window.components["FileList_fileFounded"].selectors)
               selector = Selector(f"fileFounded-{file}",[0,height * 20],[app.current_window.components["FileList_fileFounded"].rect.width - 20 , 20],{"stringvalue":file , "padding left":20 , "color":[255 , 255 , 255]} , path+"\\"+file)
               
               app.current_window.components["FileList_fileFounded"].selectors.append(selector)
     except:
          pass
     
def add_file():
     image = Image([0,0])
     
     try:
          selector = None
          for select in app.current_window.components["FileList_fileFounded"].selectors:
               if select.selected:
                    selector = select
          
          if selector == None:
               return
               
          image.load(selector.value)
          height = len(app.panels["File list"].selectors)
          oc = ""
          oc_number = 0
          for select in app.panels["File list"].selectors:
               if select.value.name == image.name:
                    oc_number += 1
          
          if oc_number != 0:
               oc = f" ( {oc_number} )"
          selector = Image_selector(f"img-{image.name}",[0,height * 20],[app.panels["File list"].rect.width - 20 , 20],{"stringvalue":image.name+oc , "padding left":20 , "color":[255 , 255 , 255]} , image)
          
          selector.target = load_image
          app.panels["File list"].selectors.append(selector)
          
          close_window(app.current_window)
     except:
          pass


def load_image(image):
     
     app.panels["Img displayer"].image = image 
     app.panels["Img displayer"].resize()

def remove_ffl(selector):
     
     index = app.panels["File list"].selectors.index(selector)
     app.panels["File list"].selectors.remove(selector)
     
     if app.panels["File list"].selectors == []:
          app.panels["Img displayer"].image = Image([0,0])
     else :
          try:
               app.panels["Img displayer"].image = app.panels["File list"].selectors[index].value
               app.panels["Img displayer"].resize()
          except:
               app.panels["Img displayer"].image = app.panels["File list"].selectors[index - 1].value
               app.panels["Img displayer"].resize()

def sym_hori():
     
     try:
          image_data = traitement.symHori(app.panels["Img displayer"].image.image_data)
          app.panels["Img displayer"].image.load_by_data(image_data)
     except:
          pass
          

def sym_vert():
     
     try:
          image_data = traitement.symVert(app.panels["Img displayer"].image.image_data)
          app.panels["Img displayer"].image.load_by_data(image_data)
     except:
          pass

def rot_180():
     
     try:
          image_data = traitement.rotation180(app.panels["Img displayer"].image.image_data)
          app.panels["Img displayer"].image.load_by_data(image_data)
     except:
          pass
          

def rot_90():
     
     try:
          image_data = traitement.rotation90(app.panels["Img displayer"].image.image_data)
          app.panels["Img displayer"].image.load_by_data(image_data)
     except:
          pass

def pgm_conv():
     
     try:
          image_data = traitement.conversion_ppm_en_pgm(app.panels["Img displayer"].image.image_data)
          app.panels["Img displayer"].image.load_by_data(image_data)
     except:
          pass

def pbm_conv(value,img_displayer,window):
     
     try:
          image_data = traitement.bitmap_conversion(img_displayer.image.image_data , value)
          img_displayer.image.load_by_data(image_data)
          pygame.event.post(pygame.event.Event(Window.WINDOW_CLOSED, {"window":window}))
     except:
          pass

def luminosity(value , img_displayer , window):
     
     try:
          image_data = traitement.luminosity(img_displayer.image.image_data , value)
          img_displayer.image.load_by_data(image_data)
          pygame.event.post(pygame.event.Event(Window.WINDOW_CLOSED, {"window":window}))
     except:
          pass

def saturation(value , img_displayer , window):
     
     try:
          image_data = traitement.saturation(img_displayer.image.image_data , value)
          img_displayer.image.load_by_data(image_data)
          pygame.event.post(pygame.event.Event(Window.WINDOW_CLOSED, {"window":window}))
     except:
          pass
     
def rotation(value , img_displayer , window):
     
     try:
          image_data = traitement.rotation(img_displayer.image.image_data , value)
          img_displayer.image.load_by_data(image_data)
          pygame.event.post(pygame.event.Event(Window.WINDOW_CLOSED, {"window":window}))
     except:
          pass

def resize_image():
     
     try:
          new_size = [int(app.panels["Tool panel"].panels["main tools"].components["entry_xSize"].stringValue) , int(app.panels["Tool panel"].panels["main tools"].components["entry_ySize"].stringValue)]
          image_data = traitement.resize_image(app.panels["Img displayer"].image.image_data , new_size)
          app.panels["Img displayer"].image.load_by_data(image_data)
     except:
          pass
def extend(package):
     
     if package.case:
          package.case = 0
     else:
          package.case = 1
     