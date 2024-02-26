

"""
    Proyecto Final PDSeI- Deteccion y reconocimiento de Placas Vehiculares
"""

from ultralytics import YOLO
import cv2

from sort.sort import *
from util import get_car, read_license_plate, write_csv


results = {}

mot_tracker = Sort()

# Modelos
coco_model = YOLO('./yolov8n.pt')
license_plate_detector = YOLO('./models/best_120_2000.pt')

# Clases
vehicles = [2,  # Auto
            3,  # Moto
            5,  # Autobús
            7]  # Camión


# Video
cap = cv2.VideoCapture('./video_carros_3ra_puerta.mp4')

# WEBCAM
#cap = cv2.VideoCapture(2)

# ret = True
while True:
    try:
        # Leemos fotogramas
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(frame, (1280, 720))

        detections = coco_model(frame)[0]
        detections_ = []

        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:
                detections_.append([x1, y1, x2, y2, score])

        # Seguimiento de Vehiculos
        track_ids = mot_tracker.update(np.asarray(detections_))

        # Detectamos matriculas
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # Asignamos la matricula al vehiculo
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

            if car_id != -1:

                # Recorte a la matricula
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
                license_plate_crop = cv2.resize(license_plate_crop, (int((x2 - x1) * 80 / (y2 - y1)), 80))

                # Aplicamos filtros
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)


                # Obteción del texto de la matricula
                
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

             
                if license_plate_text is not None:

                    try:
                        results[frame][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                      'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                        'text': license_plate_text,
                                                                        'bbox_score': score,
                                                                        'text_score': license_plate_text_score}}
                    except:
                        pass

        # Muestra el video
        # cv2.imshow('LPR-UNT', frame)

        if cv2.waitKey(1) == 27:
            break
    except:
        pass

cap.release()
cv2.destroyAllWindows()
# Guardamos los resultados
write_csv(results, './test.csv')