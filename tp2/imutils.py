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

def contar_circulos(imagen):
   '''
   Recibe una imagen y devuelve la cantidad de círculos que hay en ella.
   '''
   imagen = cv2.medianBlur(imagen, 7)

   circles = cv2.HoughCircles(imagen,
                              cv2.HOUGH_GRADIENT,
                              1, 20,
                              param1=50, param2=50,
                              minRadius=20, maxRadius=50)

   n = 0

   if isinstance(circles, np.ndarray):
      n = len(circles[0])

   return n

def graficar_caja(img, stats, color, box=True, text=None,
                  thickness=3, fontScale=10):
   '''
   Función para graficar un boundig box 
   sobre una imagen dada.
   '''

   left   = stats[cv2.CC_STAT_LEFT]
   top    = stats[cv2.CC_STAT_TOP]
   width  = stats[cv2.CC_STAT_WIDTH]
   height = stats[cv2.CC_STAT_HEIGHT]

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
                  color=color,
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

def rellenar(img):
   '''
   Recibe una imagen binaria, devuelve la misma imagen con
   las formas huecas rellenas.
   '''
   img_flood_fill = img.copy().astype('uint8')
   h, w = img.shape[:2]
   mask = np.zeros((h+2, w+2), np.uint8)
   cv2.floodFill(img_flood_fill, mask, (0,0), 255)
   img_flood_fill_inv = cv2.bitwise_not(img_flood_fill)
   img_fh = img | img_flood_fill_inv
   return img_fh 