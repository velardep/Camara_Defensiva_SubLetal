import cv2
import numpy as np
import serial
import time
from ultralytics import YOLO
import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)
engine.setProperty('volume', 1.0)  # Asegura volumen al máximo

# Asegura que se use el dispositivo predeterminado de salida (altavoces externos configurados en Windows)
# Nota: pyttsx3 no permite seleccionar un dispositivo de salida directamente.
# Se debe configurar el dispositivo de reproducción predeterminado en el sistema operativo.

# -----------------------------------------
# CENTROS MANUALES CONFIGURABLES
# -----------------------------------------
centroX = 115
centroY = 60

# -----------------------------------------
# CONEXIÓN SERIAL Y CENTRADO INICIAL + AUDIO
# -----------------------------------------
try:
    esp = serial.Serial('COM3', 115200)
    time.sleep(2)
    print("[✓] Conectado a ESP32")

    def anunciar_inicio():
        engine.say("Sistema activado, permiso de ataque recibido, procediendo a modo vigilancia")
        engine.runAndWait()

    comando_centro = f"X:{centroX} Y:{centroY}\n"
    esp.write(comando_centro.encode())
    print(f"[↻] Centrando servos en X:{centroX} Y:{centroY}")

    threading.Thread(target=anunciar_inicio, daemon=True).start()
    time.sleep(0.5)

except Exception as e:
    esp = None
    print(f"[X] Error al conectar al ESP32: {e}")

# -----------------------------------------
# MODELO + VIDEO
# -----------------------------------------
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(1)
cap.set(3, 960)
cap.set(4, 720)

# -----------------------------------------
# MAPEO
# -----------------------------------------
def mapear_con_centro(valor, centro_px, in_min, in_max, centro_servo, rango):
    desplazamiento = valor - centro_px
    porcentaje = desplazamiento / ((in_max - in_min) / 2)
    return int(np.clip(centro_servo + porcentaje * rango, 0, 180))

# -----------------------------------------
# VARIABLES
# -----------------------------------------
angX_actual = centroX
angY_actual = centroY
umbral_mov = 1.5
frame_count = 0
prev_time = time.time()

contador_alertas = 0
tiempo_ultima_alerta = 0
tiempo_entre_alertas = 1.5  # segundos
sonando = False

# -----------------------------------------
# LOOP
# -----------------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("[X] No se pudo capturar imagen")
        break

    frame_count += 1
    if frame_count % 2 != 0:
        continue

    frame_h, frame_w = frame.shape[:2]
    centro_px = frame_w // 2
    centro_py = frame_h // 2

    results = model(frame, verbose=False)[0]
    boxes = [box for box in results.boxes if int(box.cls[0]) == 0 and box.conf[0] > 0.5]

    persona_objetivo = None
    max_area = 0

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cx = (x1 + x2) // 2
        cy = y1 + int((y2 - y1) * 0.35)
        area = (x2 - x1) * (y2 - y1)

        if area > max_area:
            max_area = area
            persona_objetivo = (x1, y1, x2, y2, cx, cy)

    color = (0, 255, 0)
    texto_estado = "Estado: Sin movimiento"

    if persona_objetivo:
        x1, y1, x2, y2, cx, cy = persona_objetivo

        angX = mapear_con_centro(cx, centro_px, 0, frame_w, centroX, rango=60)
        angY = mapear_con_centro(cy, centro_py, 0, frame_h, centroY, rango=60)

        if abs(angX - angX_actual) > umbral_mov or abs(angY - angY_actual) > umbral_mov:
            comando = f"X:{angX} Y:{angY}\n"
            print(f"[→] Enviando: {comando.strip()}")
            if esp:
                esp.write(comando.encode())
            angX_actual = angX
            angY_actual = angY

        ahora = time.time()

        if ahora - tiempo_ultima_alerta > tiempo_entre_alertas and not sonando:
            if contador_alertas == 0:
                def aviso1():
                    global sonando
                    sonando = True
                    engine.say("Advertencia: Usted está ingresando a una zona restringida. Abandone el área.")
                    engine.runAndWait()
                    sonando = False
                threading.Thread(target=aviso1, daemon=True).start()
                contador_alertas += 1
                tiempo_ultima_alerta = ahora

            elif contador_alertas == 1:
                def aviso2():
                    global sonando
                    sonando = True
                    engine.say("Segunda advertencia, retroceda o será atacado.")
                    engine.runAndWait()
                    sonando = False
                threading.Thread(target=aviso2, daemon=True).start()
                contador_alertas += 1
                tiempo_ultima_alerta = ahora

            elif contador_alertas == 2:
                sonando = True
                engine.say("Última advertencia")
                engine.runAndWait()
                sonando = False
                contador_alertas += 1
                tiempo_ultima_alerta = ahora

        texto_estado = "Persona Detectada"
        color = (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.circle(frame, (centro_px, centro_py), 5, (255, 0, 0), -1)

    else:
        contador_alertas = 0
        sonando = False

    fps = int(1 / (time.time() - prev_time + 0.0001))
    prev_time = time.time()
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
    cv2.putText(frame, f"{texto_estado} | FPS: {fps}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("YOLOv8 - Seguimiento Rápido", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
