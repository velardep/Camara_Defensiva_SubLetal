<p align="center">
  <img src="https://raw.githubusercontent.com/velardep/Camara_Defensiva_SubLetal/main/docs/logo.png" alt="Logo Camara Defensiva" width="300"/>
</p>

# Sistema de Cámara Defensiva Subletal

Sistema integrado para detección de movimientos en tiempo real mediante visión artificial y control de hardware. Este proyecto utiliza Python para procesamiento de video y detección, y C++ para el manejo de microcontroladores y servomotores que activan un mecanismo de disparo disuasivo.

---

## Descripción

Este sistema consta de dos partes principales que deben ejecutarse de forma secuencial para un correcto funcionamiento:

1. **Control de servomotores y microcontrolador ESP32:** Se carga y ejecuta el firmware en el ESP32 para controlar los servos y el mecanismo físico de disparo. Esta parte debe ejecutarse primero y, al finalizar, el proceso se detiene.

2. **Sistema de detección y control en Python:** Luego de detener el firmware, se ejecuta el código Python que inicia la transmisión en vivo, detecta movimientos en la zona definida usando YOLO, envía alertas y activa los servos mediante el microcontrolador cuando sea necesario.

Mientras el código Python esté en ejecución, el sistema funcionará en tiempo real activando las alertas y el mecanismo disuasivo.

---

## Características principales

- Detección en tiempo real de movimientos en zona segura usando visión artificial con YOLO.
- Control preciso de servomotores mediante ESP32 para mover la cámara y activar disparos disuasivos.
- Integración completa de software (Python y C++) y hardware (microcontroladores, servos y soporte físico).
- Diseño y fabricación del soporte físico de la cámara con SolidWorks e impresión 3D.

---

## Tecnologías usadas

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++" />
  <img src="https://img.shields.io/badge/PlatformIO-2D9EE0?style=for-the-badge&logo=platformio&logoColor=white" alt="PlatformIO" />
</p>


- Python (OpenCV, YOLO para detección de movimiento).
    <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    </p>
- C++ para firmware en ESP32 (control de servomotores).
    <p>
    <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++" />
    </p>
- Extensión PlatformIO IDE
    <p>
    <img src="https://img.shields.io/badge/PlatformIO-2D9EE0?style=for-the-badge&logo=platformio&logoColor=white" alt="PlatformIO" />
    </p>

- SolidWorks para modelado 3D.
- Impresión 3D para fabricación del soporte físico.
- Git para control de versiones.

---

## Instalación y ejecución

### Requisitos previos

- Visual Studio Code instalado.
- Extensión **PlatformIO IDE** instalada para programar y cargar firmware en ESP32.
- Python 3.8 o superior instalado en el sistema.
- Drivers para ESP32 instalados (PlatformIO usualmente los maneja).
- Librerías Python necesarias según `requirements.txt`.

---

### Pasos para iniciar el sistema en Visual Studio Code

1. **Abrir el proyecto**

   - Abre la carpeta del proyecto en Visual Studio Code.

2. **Ejecutar y cargar firmware en ESP32 (control de servos)**

   - En Visual Studio Code, abre la pestaña de PlatformIO.
   - En “Project Tasks”, selecciona el entorno ESP32.
   - Haz clic en `Build` para compilar el firmware.
   - Luego haz clic en `Upload` para cargarlo al ESP32 conectado.
   - Después de cargar, **ejecuta el firmware desde PlatformIO** para controlar los servos.
   - **Una vez que el proceso de control de servos finalice, detén la ejecución manualmente en PlatformIO** (parar tarea).

3. **Instalar librerías Python**

   - Abre una terminal en Visual Studio Code.
   - Ejecuta:

     ```bash
     pip install -r requirements.txt
     ```

4. **Ejecutar el script Python (detección y disparo)**

   - En la misma terminal, ejecuta:

     ```bash
     python main.py
     ```

---

**Nota:** El sistema funciona en dos fases separadas: primero, se ejecuta el firmware en el ESP32 que controla los servos; una vez que ese proceso termina y es detenido, se inicia el script Python que realiza la detección, genera alertas y activa el mecanismo de disparo mediante el ESP32. Mientras el script Python esté en ejecución, el sistema estará activo y funcionando correctamente.
