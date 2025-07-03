import cv2
import numpy as np

# Iniciar la webcam (0 para cámara integrada)
cap = cv2.VideoCapture(0)

# Opcional: fijar resolución
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Inicializar sustracción de fondo (detección de movimiento)
fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Aplicar la sustracción de fondo
    fgmask = fgbg.apply(frame)

    # Limpiar ruido con operaciones morfológicas
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    # Buscar contornos en la máscara
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar contornos con forma de cuerpo humano
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 800:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)

            if 0.2 < aspect_ratio < 0.6 and h > 50:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Mostrar resultados
    cv2.imshow("Detección de Personas - Webcam", frame)
    cv2.imshow("Máscara de Movimiento", fgmask)

    # Salir con tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
