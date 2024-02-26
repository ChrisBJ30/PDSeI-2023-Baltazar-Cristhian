
import cv2
import numpy as np

def sauvola_threshold(img, window_size=25, k=0.25, R=128):
    # Convertir la imagen a escala de grises si no lo está
    if len(img.shape) > 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Definir la imagen de salida
    output_img = np.zeros_like(img)

    # Calcular el radio de la ventana
    radius = window_size // 2

    # Iterar sobre cada píxel de la imagen
    for y in range(radius, img.shape[0] - radius):
        for x in range(radius, img.shape[1] - radius):
            # Calcular la media y la desviación estándar de la región
            region = img[y - radius:y + radius + 1, x - radius:x + radius + 1]
            mean = np.mean(region)
            std_dev = np.std(region)

            # Calcular el umbral de Sauvola
            threshold = mean * (1 + k * ((std_dev / R) - 1))

            # Binarizar el píxel
            if img[y, x] > threshold:
                output_img[y, x] = 255
            else:
                output_img[y, x] = 0
    return 255-output_img


def apply_gaussian_and_adaptive_threshold(gray_image):
    # Aplicar filtro gaussiano
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 3)
    # Aplicar binarización adaptativa
    adaptive_thresh = cv2.adaptiveThreshold(
        blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19, 22)
    return adaptive_thresh

def morphology_op(img):
    # Crear el kernel
    kernel = np.ones((4,4),np.uint8)
    # Aplicar la operación de apertura
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return opening
def morphology_cl(img):
    # Crear el kernel
    kernel = np.ones((4,4),np.uint8)
    # Aplicar la operación de apertura
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return closing

