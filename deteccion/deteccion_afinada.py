import cv2
import numpy as np

cap = cv2.VideoCapture('video.mp4')

fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensionar para evitar errores al mostrar
    frame = cv2.resize(frame, (960, 720))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
    color = (0, 255, 0)
    texto_estado = "Estado: No se ha detectado movimiento"

    # Zona de análisis
    area_pts = np.array([[240, 400], [660, 400], [730, frame.shape[0]], [230, frame.shape[0]]])
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_and(gray, gray, mask=imAux)

    # Procesamiento de movimiento
    fgmask = fgbg.apply(image_area)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for cnt in cnts:
        if cv2.contourArea(cnt) > 1500:
            x, y, w, h = cv2.boundingRect(cnt)

            # Punto medio (centro del cuerpo)
            cx = x + w // 2
            cy = y + h // 2

            # Dibuja rectángulo y punto central
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

            # Mostrar coordenadas por consola
            print(f"Centro del cuerpo detectado en: ({cx}, {cy})")

            texto_estado = "Estado: Alerta Movimiento Detectado!"
            color = (0, 0, 255)

    # Zona visual y texto
    cv2.drawContours(frame, [area_pts], -1, color, 2)
    cv2.putText(frame, texto_estado, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow('fgmask', fgmask)
    cv2.imshow("frame", frame)

    k = cv2.waitKey(120) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
