import numpy as np
import cv2

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