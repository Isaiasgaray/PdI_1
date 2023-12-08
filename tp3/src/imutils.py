import numpy as np
import cv2

def calcular_factor_forma(img):
   '''
   Recibe una sub-imagen y devuelve su factor de forma
   '''
   ext_cont, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   area = cv2.contourArea(ext_cont[0])
   perimeter = cv2.arcLength(ext_cont[0], True)
   rho = 4 * np.pi * area /(perimeter ** 2)
   return rho

def contar_contornos(img_bin):
   '''
   Recibe una imagen binaria y devuelve la cantidad
   de contornos que hay en ella
   '''

   contours, _ = cv2.findContours(img_bin,
                                  cv2.RETR_LIST,
                                  cv2.CHAIN_APPROX_SIMPLE)

   return len(contours)

def graficar_caja(img, stats, color, box=True, text=None,
                  thickness=3, fontScale=10, color_text=None):
   '''
   Función para graficar un boundig box 
   sobre una imagen dada.
   '''

   left   = stats[cv2.CC_STAT_LEFT]
   top    = stats[cv2.CC_STAT_TOP]
   width  = stats[cv2.CC_STAT_WIDTH]
   height = stats[cv2.CC_STAT_HEIGHT]

   if not color_text:
      color_text = color

   if box:
      cv2.rectangle(img, 
                    (left, top), 
                    (left + width,top + height),
                    color=color, thickness=thickness)
      
   if text:
      cv2.putText(img, text, 
                  (left, top - 10),
                  cv2.FONT_HERSHEY_SIMPLEX,
                  fontScale=fontScale,
                  color=color_text,
                  thickness=thickness)

def obtener_sub_imagen(img, stats):
    '''
    Recibe una imagen y stats sobre un área de interés,
    devuelve la sub-imagen correspondiente a esa área.
    '''

    coor_h = stats[cv2.CC_STAT_LEFT] 
    coor_v = stats[cv2.CC_STAT_TOP]

    ancho  = stats[cv2.CC_STAT_WIDTH]   
    largo  = stats[cv2.CC_STAT_HEIGHT]

    return img[coor_v:coor_v + largo, coor_h: coor_h + ancho]

def leer_video(path):
    '''
    Recibe un path a un video y devuelve
    el objeto necesario para iterar sobre sus
    frames y otras variable con información del video.

    Devuelve:
    cap, width, height, fps, n_frames
    '''
    cap      = cv2.VideoCapture(path)
    width    = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
    height   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps      = int(cap.get(cv2.CAP_PROP_FPS))
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    return cap, width, height, fps, n_frames
