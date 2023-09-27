import cv2
import numpy as np
import matplotlib.pyplot as plt

def ecualizacion_local_histograma(imagen, tamano_ventana):
    alto, ancho = imagen.shape
    mitad_ventana = tamano_ventana // 2

    # Agregar bordes para manejar los pixeles cercanos a los bordes de la imagen
    imagen_con_bordes = cv2.copyMakeBorder(imagen, mitad_ventana, mitad_ventana, mitad_ventana, mitad_ventana, cv2.BORDER_REPLICATE)

    imagen_resultado = np.zeros_like(imagen, dtype=np.uint8)
    
    for i in range(mitad_ventana, alto + mitad_ventana):
        for j in range(mitad_ventana, ancho + mitad_ventana):
            ventana = imagen_con_bordes[i-mitad_ventana:i+mitad_ventana+1, j-mitad_ventana:j+mitad_ventana+1]
            hist, _ = np.histogram(ventana.flatten(), bins=256, range=(0,256), density=True)
            cdf = hist.cumsum()
            cdf_normalizado = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
            imagen_resultado[i-mitad_ventana, j-mitad_ventana] = cdf_normalizado[ventana[mitad_ventana, mitad_ventana]]

    return imagen_resultado

ruta_imagen = 'imagen_con_detalles_escondidos.tif'
imagen_original = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

tamano_ventana = 30

imagen_procesada = ecualizacion_local_histograma(imagen_original, tamano_ventana)

plt.figure(figsize=(10,5))
plt.subplot(121)
plt.title('Imagen Original')
plt.imshow(imagen_original, cmap='gray')
plt.subplot(122)
plt.title('Resultado')
plt.imshow(imagen_procesada, cmap='gray')
plt.show(block=False)