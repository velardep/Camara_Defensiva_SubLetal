import serial
import time

# Reemplaza 'COM3' con tu puerto real si es distinto
puerto = 'COM3'
baudrate = 115200

# Abrir conexión serial con el ESP32-S3
esp = serial.Serial(puerto, baudrate)
time.sleep(2)  # Espera a que el ESP32 inicie

# Enviar un ángulo de prueba
angulo = 45  # Cambia a cualquier valor entre 0 y 180
comando = f'X:{angulo}\n'
esp.write(comando.encode())
print(f"Comando enviado: {comando.strip()}")

esp.close()
