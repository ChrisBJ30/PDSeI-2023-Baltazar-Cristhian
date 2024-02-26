
from ultralytics import YOLO
import cv2
from matplotlib import pyplot as plt
import numpy as np
import filters
from filters import apply_gaussian_and_adaptive_threshold, sauvola_threshold, morphology_op, morphology_cl
from formatocr import read_license_plate

model = YOLO('./models/best_120_2000.pt')

image = cv2.imread('./TEST/3.jpg')
# image = cv2.imread('./imgt/6.jpg')

license_plates = model(image)[0]
x1 = 0
x2 = 0
y1 = 0
y2 = 0
score = 0

for license_plate in license_plates.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = license_plate

license_plate_crop = image[int(y1):int(y2), int(x1):int(x2), :]

# ESCALA DE GRISES
license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)

# FILTRO THRESHOLD
_, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

# FILTRO GAUSSIANO-BINN_ADP
license_plate_crop_gauss = apply_gaussian_and_adaptive_threshold(license_plate_crop_gray)

# FILTRO SAUVOLA
license_plate_crop_sauvola = sauvola_threshold(license_plate_crop_gray)

#------------------- APERTURA MORFOLOGICA ------------------- license_plate_crop_thresh = morphology_op(license_plate_crop_thresh)
license_plate_crop_gauss = morphology_op(license_plate_crop_gauss)
license_plate_crop_sauvola = morphology_op(license_plate_crop_sauvola)


# images = [license_plate_crop_thresh, 0,
#           license_plate_crop_gauss, 0,
#           license_plate_crop_sauvola,0]
# titles = ['Thresh', 'Histogram',
#           'Gauss', 'Histogram',
#           "Sauvola", 'Histogram']

# for i in range(3):
#     plt.subplot(3,2,i*2+1),plt.imshow(images[i*2],'gray')
#     plt.title(titles[i*2]), plt.xticks([]), plt.yticks([])
#     plt.subplot(3,2,i*2+2),plt.hist(images[i*2].ravel(),256)
#     plt.title(titles[i*2+1]), plt.xticks([]), plt.yticks([])
# plt.show()

#------------------- EASYOCR -------------------
text, score = read_license_plate(cv2.resize(license_plate_crop_thresh,(640,480)))
# text1, score1 = read_license_plate(cv2.resize(license_plate_crop_gauss,(640,480)))
# text2, score2 = read_license_plate(cv2.resize(license_plate_crop_sauvola,(640,480)))
print(f'Score: {score}')
print(f'PLACA M1: {text}')
# print('Método 2')
# print(f'Score: {score1}')
# print(f'License Plate Number: {text1}')
# print('Método 3')
# print(f'Score: {score2}')
# print(f'License Plate Number: {text2}')

#------------------- PYTESSERACT -------------------
# import pytesseract
# # If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#
# textp = pytesseract.image_to_string(license_plate_crop_thresh, config='--psm 11')
# textp1 = pytesseract.image_to_string(cv2.resize(license_plate_crop_gauss,(640,480)), config='--psm 11')
# textp2 = pytesseract.image_to_string(cv2.resize(license_plate_crop_sauvola,(640,480)), config='--psm 11')
#
# print('PLACA M1:', textp)
# print('PLACA M2: ', textp1[:7])
# print('PLACA M3: ', textp2[:7])

