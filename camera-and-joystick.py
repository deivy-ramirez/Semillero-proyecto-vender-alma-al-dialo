import cv2
import pygame
import numpy as np

# Inicializar pygame y configurar la pantalla
pygame.init()
pygame.joystick.init()
dimensiones = [1280, 920]  # Ventana más grande para acomodar todo
pantalla = pygame.display.set_mode(dimensiones)
pygame.display.set_caption("Control de Joystick y Cámara")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Clase para imprimir texto en pantalla
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def print(self, pantalla, texto):
        text_bitmap = self.font.render(texto, True, NEGRO)
        pantalla.blit(text_bitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 650  # Movemos el texto a la derecha para dejar espacio para la cámara
        self.y = 10
        self.line_height = 30

# Verificar joystick
if pygame.joystick.get_count() == 0:
    print("No se detectó ningún joystick")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Variables de control
camara_activa = False
cap = None
text_print = TextPrint()
reloj = pygame.time.Clock()

def abrir_camara():
    global cap, camara_activa
    if not camara_activa:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("No se puede abrir la cámara")
            return False
        camara_activa = True
        return True
    return False

def cerrar_camara():
    global cap, camara_activa
    if camara_activa:
        cap.release()
        camara_activa = False

def frame_a_surface(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir BGR a RGB
    frame = cv2.resize(frame, (640, 480))  # Redimensionar a un tamaño fijo
    frame = np.rot90(frame)  # Rotar si es necesario
    frame = pygame.surfarray.make_surface(frame)
    return frame

# Bucle principal
hecho = False
while not hecho:
    # Procesar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho = True
        elif evento.type == pygame.JOYBUTTONDOWN:
            if joystick.get_button(2):
                if not camara_activa:
                    abrir_camara()
            if joystick.get_button(0):
                if camara_activa:
                    cerrar_camara()

    # Limpiar pantalla
    pantalla.fill(BLANCO)
    text_print.reset()

    # Mostrar imagen de la cámara si está activa
    if camara_activa:
        ret, frame = cap.read()
        if ret:
            # Convertir el frame de OpenCV a surface de Pygame
            frame_surface = frame_a_surface(frame)
            # Mostrar en la esquina superior izquierda
            pantalla.blit(frame_surface, (0, 0))
        else:
            print("No se pudo recibir frame")
            cerrar_camara()

    # Obtener y mostrar datos del joystick
    text_print.print(pantalla, f"Joystick: {joystick.get_name()}")
    text_print.print(pantalla, f"Número de botones: {joystick.get_numbuttons()}")
    
    for i in range(joystick.get_numbuttons()):
        text_print.print(pantalla, f"Botón {i}: {joystick.get_button(i)}")

    # Ejes
    text_print.print(pantalla, f"Número de ejes: {joystick.get_numaxes()}")
    for i in range(joystick.get_numaxes()):
        text_print.print(pantalla, f"Eje {i}: {joystick.get_axis(i):.6f}")

    # Hats (D-pad)
    text_print.print(pantalla, f"Número de hats: {joystick.get_numhats()}")
    for i in range(joystick.get_numhats()):
        text_print.print(pantalla, f"Hat {i}: {joystick.get_hat(i)}")

    # Estado de la cámara
    text_print.print(pantalla, f"Cámara activa: {camara_activa}")
    """text_print.print(pantalla, "Botón 2: Abrir cámara")
    text_print.print(pantalla, "Botón 0: Cerrar cámara")"""

    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(60)

# Limpieza final
cerrar_camara()
pygame.quit()