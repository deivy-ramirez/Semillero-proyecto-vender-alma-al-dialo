import cv2

# Abrir la cámara (0 es el primer dispositivo)
cap = cv2.VideoCapture(0)

# Verificar si la cámara se abrió correctamente
if not cap.isOpened():
    print("No se puede abrir la cámara")
    exit()

# Bucle para mostrar el video en tiempo real
while True:
    # Capturar frame por frame
    ret, frame = cap.read()

    # Si no se pudo leer el frame
    if not ret:
        print("No se pudo recibir frame (stream finalizado)")
        break

    # Mostrar el frame
    cv2.imshow('Real-Time Video', frame)

    # Presionar 'q' para salir
    if cv2.waitKey(1) == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()