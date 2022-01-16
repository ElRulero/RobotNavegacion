# Importamos las librerías relevantes
import cv2
# Librería auxiliar para llevar a cabo operaciones que suelen ser engorrosas en OpenCV
import imutils
import mahotas
import numpy as np


def load_digits(dataset_path):
    """
    Carga el conjunto de datos.
    :param dataset_path: Ruta del conjunto de datos en formato CSV.
    :return: Dos tensores. El primero correspondientes a las imágenes en escala de grises de MNIST y el segundo
             a las etiquetas.
    """
    # Cargamos los datos a arreglos de NumPy.
    images = np.genfromtxt(dataset_path, delimiter=',', dtype='uint8')
    labels = images[:, 0]  # La primera columna corresponde a la etiqueta.

    # Las columnas restantes corresponden a los 28x28=784 pixeles de cada imagen.
    images = images[:, 1:].reshape(images.shape[0], 28, 28)

    return images, labels


def deskew(image, width):
    """
    Endereza el contenido de una imagen.
    :param image: Imagen cuyo contenido enderezaremos.
    :param width: Ancho objetivo de la imagen resultante. La altura será calculada automáticamente para preservar
                  la relación de aspecto.
    :return: Imagen enderezada.
    """
    (h, w) = image.shape[:2]

    # Calculamos los momentos estadísticos de la imagen.
    moments = cv2.moments(image)

    # El grado de "sesgo" o inclinación de la imagen viene dado por el cociente de ambos momentos.
    skew = moments['mu11'] / moments['mu02']

    # Definimos la matriz de enderezamiento.
    M = np.float32([[1, skew, -0.5 * w * skew], [0, 1, 0]])

    # Endereza la imagen usando la matriz de transformación.
    image = cv2.warpAffine(image, M, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)

    # Redimensiona la imagen manteniendo la relación de aspecto.
    image = imutils.resize(image, width=width)

    return image


def center_extent(image, size):
    """
    Centra el contenido de una imagen.
    :param image: Imagen cuyo contenido centraremos.
    :param size: Tamaño de la imagen final.
    :return: Imagen con contenido centrado.
    """
    (e_w, e_h) = size

    # Resimensionamos acorde a la dimensión más grande.
    if image.shape[1] > image.shape[0]:
        image = imutils.resize(image, width=e_w)
    else:
        image = imutils.resize(image, height=e_h)

    # Creamos la iamgen de salida.
    extent = np.zeros((e_h, e_w), dtype='uint8')

    # Calculamos el desplazamiento en ambas direcciones necesario para centrar la imagen.
    offset_x = (e_w - image.shape[1]) // 2
    offset_y = (e_h - image.shape[0]) // 2

    # Ubicamos la imagen original en la nueva.
    extent[offset_y:offset_y + image.shape[0], offset_x:offset_x + image.shape[1]] = image

    # Calculamos el centro de masa.
    cm = mahotas.center_of_mass(extent)
    (c_y, c_x) = np.round(cm).astype('int32')
    (d_x, d_y) = ((size[0] // 2) - c_x, (size[1] // 2) - c_y)

    # Desplazamos el contenido de la imagen al centro.
    M = np.float32([[1, 0, d_x], [0, 1, d_y]])
    extent = cv2.warpAffine(extent, M, size)

    return extent
