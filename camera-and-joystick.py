"""
import cv2
import pygame

# Inicializar pygame y el joystick
pygame.init()
pygame.joystick.init()

# Verificar si hay joysticks/gamepads conectados
if pygame.joystick.get_count() == 0:
    print("No se detectó ningún joystick")
    exit()

# Inicializar el primer joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Variables de control
camara_activa = False
cap = None

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
        cv2.destroyAllWindows()
        camara_activa = False

# Bucle principal
while True:
    # Procesar eventos de pygame
    for evento in pygame.event.get():
        if evento.type == pygame.JOYBUTTONDOWN:
            # Botón 2 para abrir la cámara
            if joystick.get_button(2):
                if not camara_activa:
                    abrir_camara()
            
            # Botón 0 para cerrar la cámara
            if joystick.get_button(0):
                if camara_activa:
                    cerrar_camara()

    # Si la cámara está activa, mostrar el video
    if camara_activa:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo recibir frame (stream finalizado)")
            cerrar_camara()
            continue

        cv2.imshow('Real-Time Video', frame)

        # Verificar si se presiona 'q' para salir
        if cv2.waitKey(1) == ord('q'):
            break

# Limpieza final
cerrar_camara()
pygame.quit()

"""
import cv2
import pygame

# Inicializar pygame y configurar la pantalla
pygame.init()
pygame.joystick.init()
dimensiones = [500, 700]
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
        self.x = 10
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
        cv2.destroyAllWindows()
        camara_activa = False

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

    # Obtener y mostrar datos del joystick
    # Botones
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

    # Actualizar pantalla
    pygame.display.flip()

    # Si la cámara está activa, mostrar el video
    if camara_activa:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo recibir frame")
            cerrar_camara()
            continue

        cv2.imshow('Real-Time Video', frame)
        if cv2.waitKey(1) == ord('q'):
            hecho = True

    reloj.tick(60)

# Limpieza final
cerrar_camara()
pygame.quit()