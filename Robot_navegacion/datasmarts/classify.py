# Importamos las depenencias.
import pickle
from argparse import ArgumentParser

import cv2
import mahotas

# Estas son las dependencias implementadas por nosotros.
from datasmarts.dataset import dataset
from datasmarts.feature.hog import HOG

# Definimos el menú del script:
# * -m/--model: Ruta al clasificador.
# * -i/--image: Ruta a la imagen a procesar.
argument_parser = ArgumentParser()
argument_parser.add_argument('-m', '--model', required=True, help='Ruta al modelo.')
argument_parser.add_argument('-i', '--image', required=True, help='Ruta a la imagen de entrada.')
arguments = vars(argument_parser.parse_args())

# Cargamos el modelo entrenado.
with open(arguments['model'], 'rb') as f:
    model = pickle.load(f)

# Creamos el extractor HOG con la misma configuración que cuando entrenamos el clasificador.
hog = HOG(orientations=18, pixels_per_cell=(10, 10), cells_per_block=(1, 1), transform=True)

# Leemos la imagen de entrada y la convertimos en escala de grises.
image = cv2.imread(arguments['image'])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicamos difuminado Gaussiano para reducir el ruido.
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Calculamos los bordes usando el algoritmo de Canny.
edged = cv2.Canny(blurred, 30, 150)

# Con base a los bordes, encontramos los contornos de los posibles dígitos.
(contours, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Ordenamos los contornos de izquierda a derecha.
contours = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda p: p[1])

# Iteramos sobre cada contorno.
for c, _ in contours:
    # Obtenemos el rectángulo que encierra a cada contorno.
    x, y, width, height = cv2.boundingRect(c)

    # Como sabemos que los dígitos son más anchos que largos, nos quedaremos con aquellos que tengan
    # dimensiones mayores o iguales a 20x7
    if width >= 7 and height >= 20:
        # Extraemos la región de interés, utilizando las coordenadas del rectángulo.
        roi = gray[y:y + height, x:x + width]
        thresh = roi.copy()

        # Usamos thresholding para convertir la región de interés en una imagen binaria, como
        # las de MNIST.
        T = mahotas.thresholding.otsu(roi)
        thresh[thresh > T] = 255
        thresh = cv2.bitwise_not(thresh)

        # Corregimos el sesgo y centramos el dígito.
        thresh = dataset.deskew(thresh, width=20)
        thresh = dataset.center_extent(thresh, size=(20, 20))

        # Mostramos la imagen binaria.
        cv2.imshow('No. binario', thresh)

        # Calculamos el vector característico usando HOG y lo pasamos al clasificador.
        histogram = hog.describe(thresh)
        digit = model.predict([histogram])[0]

        # Imprimimos la predicción en la consola.
        print(f'¿Acaso es un {digit}?')

        # Encerramos el área de interés en la imagen original, e imprimimos la predicción al lado.
        cv2.rectangle(image, (x, y), (x + width, y + height), (128, 0, 128), 1)
        cv2.putText(image,
                    text=str(digit),
                    org=(x - 10, y - 10),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.2,
                    color=(128, 0, 128),
                    thickness=2)
        cv2.imshow('image', image)
        cv2.waitKey(0)
