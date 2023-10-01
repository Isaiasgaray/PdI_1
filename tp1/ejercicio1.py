import cv2
import numpy as np
import matplotlib.pyplot as plt

def ecualizacion_local_histograma(imagen, tamano_ventana):
    alto, ancho = imagen.shape
    mitad_ventana = tamano_ventana // 2

    # Agregar bordes para manejar los pixeles cercanos a los bordes de la imagen
    imagen_con_bordes = cv2.copyMakeBorder(imagen,
                                           mitad_ventana,
                                           mitad_ventana,
                                           mitad_ventana,
                                           mitad_ventana,
                                           cv2.BORDER_REPLICATE)

    # Matriz vacia para guardar los resultados
    imagen_resultado = np.empty(imagen.shape)
    
    for i in range(mitad_ventana, alto + mitad_ventana):
        for j in range(mitad_ventana, ancho + mitad_ventana):
            ventana = imagen_con_bordes[i-mitad_ventana:i+mitad_ventana+1, j-mitad_ventana:j+mitad_ventana+1]
            
            #hist = cv2.calcHist([ventana], [0], None, [256], [0, 256])
            #cdf = hist.cumsum()
            #cdf_normalizado = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
            #imagen_resultado[i-mitad_ventana, j-mitad_ventana] = venta_equ[ventana[mitad_ventana, mitad_ventana]]
            venta_equ = cv2.equalizeHist(ventana)
            imagen_resultado[i-mitad_ventana, j-mitad_ventana] = venta_equ[mitad_ventana, mitad_ventana]

    return imagen_resultado

ruta_imagen = r'tp1\img\Imagen_con_detalles_escondidos.tif'
imagen_original = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

img1 = ecualizacion_local_histograma(imagen_original, 3*3)
img2 = ecualizacion_local_histograma(imagen_original, 11*3)
img3 = ecualizacion_local_histograma(imagen_original, 33*3)


ax1 = plt.subplot(221)
plt.title('Imagen Original')
plt.imshow(imagen_original, cmap='gray')
plt.subplot(222, sharex=ax1, sharey=ax1)
plt.title('Ventana de 3x3')
plt.imshow(img1, cmap='gray')
plt.subplot(223, sharex=ax1, sharey=ax1)
plt.title('Ventana de 9x3')
plt.imshow(img2, cmap='gray')
plt.subplot(224, sharex=ax1, sharey=ax1)
plt.title('Ventana de 33x3')
plt.imshow(img3, cmap='gray')

plt.show()
