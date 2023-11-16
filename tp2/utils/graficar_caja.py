import cv2

def graficar_caja(img, stats, color, box=True, text=None):
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
                    color=color, thickness=3)
      
   if text:
      cv2.putText(img, text, 
                  (left, top - 10),
                  cv2.FONT_HERSHEY_SIMPLEX,
                  fontScale=10,
                  color=color,
                  thickness=3)