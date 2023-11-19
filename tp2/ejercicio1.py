import matplotlib.pyplot as plt
import numpy as np
import imutils
import cv2

# Carga de imagen
PATH_MONEDAS = 'img/monedas.jpg'

img      = cv2.imread(PATH_MONEDAS)
img_rgb  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# a) Procesar la imagen de manera de segmentar las
# monedas y los dados de manera automática.
blur      = cv2.GaussianBlur(img_gray, (3, 3), 2)
img_canny = cv2.Canny(blur, 255*0.40, 255*0.70)
plt.imshow(img_canny, cmap='gray'), plt.show()

elemento_dilatacion = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 45))
img_dil = cv2.dilate(img_canny, elemento_dilatacion)
ax = plt.subplot(221)
plt.title('Dilatación - Elipse 35x45')
plt.imshow(img_dil, cmap='gray')
img_dil = imutils.rellenar(img_dil)
plt.subplot(222)
plt.title('Rellenado de bordes')
plt.imshow(img_dil, cmap='gray')

elemento_erosion = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
img_er = cv2.erode(img_dil, elemento_erosion)
plt.subplot(223)
plt.title('Erosión - Rectangulo de 10x10')
plt.imshow(img_er, cmap='gray')

elemento_cierre = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (40, 40))
img_cierre = cv2.morphologyEx(img_er, cv2.MORPH_OPEN, elemento_cierre)
plt.subplot(224)
plt.title('Operación de apertura - Elipse de 40x40')
plt.imshow(img_cierre, cmap='gray')
plt.show()

# Contamos los objetos de la máscara
n, labels, stats, _ = cv2.connectedComponentsWithStats(img_cierre)

# Matrices para las máscaras
masc_monedas = np.zeros_like(img)
masc_dados   = np.zeros_like(img)

# Listas para guardar sub-imágenes
monedas = list()
dados   = list()

RHO_TH = 0.8
MONEDAS_C = (255, 0, 0)
DADOS_C   = (0, 255, 0)

for i in range(1, n):
   obj = (labels == i).astype('uint8') * 255

   sub_imagen = imutils.obtener_sub_imagen(img_gray, stats[i])

   rho = imutils.calcular_factor_forma(obj)

   if rho >= RHO_TH:
      masc_monedas[obj == 255,] = MONEDAS_C
      monedas.append((sub_imagen, stats[i], i))
   else:
      masc_dados[obj == 255,] = DADOS_C
      dados.append((sub_imagen, stats[i], i))

# Unión de las dos máscaras
masc_monedas_dados = np.logical_or(masc_monedas, masc_dados).astype('uint8') * 255

ax = plt.subplot(221)
plt.title('Imagen original')
plt.imshow(img_rgb)
plt.subplot(222, sharex=ax, sharey=ax)
plt.title('Monedas segmentadas')
plt.imshow(np.bitwise_and(masc_monedas, img))
plt.subplot(223, sharex=ax, sharey=ax)
plt.title('Dados segmentados')
plt.imshow(np.bitwise_and(masc_dados, img))
plt.subplot(224, sharex=ax, sharey=ax)
plt.title('Objetos segmentados')
plt.imshow(np.bitwise_and(masc_monedas_dados, img))
plt.show(block=False)

# b) Clasificar los distintos tipos de monedas
# y realizar un conteo, de manera automática.

MONEDAS_S_C = (255, 0, 0)
MONEDAS_M_C = (0, 255, 0)
MONEDAS_L_C = (0, 0, 255)

monedas_s = monedas_m = monedas_l = 0

for moneda in monedas:

   ancho = moneda[0].shape[0]
   obj   = labels == moneda[2]

   # Monedas grandes, de 50 centavos
   if ancho >= 370:
      monedas_l += 1
      masc_monedas[obj == 1, :] = MONEDAS_L_C
   # Monedas chicas, de 10 centavos
   elif ancho <= 320:
      monedas_s += 1
      masc_monedas[obj == 1, ] = MONEDAS_S_C
   # El resto de las monedas son las medianas de 1 peso
   else:
      monedas_m += 1
      masc_monedas[obj == 1, ] = MONEDAS_M_C

ax = plt.subplot(221)
plt.title('Imagen original')
plt.imshow(img_rgb)
plt.subplot(222, sharex=ax, sharey=ax)
plt.title('Máscara para tipos de monedas')
plt.imshow(masc_monedas)
plt.subplot(223, sharex=ax, sharey=ax)
plt.title(f'Chicas: {monedas_s}, medianas: {monedas_m}, grandes: {monedas_l}')
plt.imshow(np.bitwise_and(masc_monedas, img))
plt.show()

# c) Determinar el número que presenta cada 
# dado mediante procesamiento automático.

ejercicio_c = img_rgb.copy()

COLOR_TEXTO = (255, 255, 255)

for dado in dados:
   n = imutils.contar_circulos(dado[0])

   imutils.graficar_caja(ejercicio_c,
                        dado[1],
                        color=COLOR_TEXTO,
                        box=False,
                        text=str(n))
   
plt.imshow(ejercicio_c), plt.title('Ejercicio 1 c'), plt.show()