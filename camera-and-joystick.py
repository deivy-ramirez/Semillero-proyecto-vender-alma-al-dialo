import pygame
import cv2
import threading

# Definimos algunos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

class TextPrint(object):
    """Esta es una sencilla clase que nos ayudará a imprimir sobre la pantalla."""
    
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)
    
    def print(self, mi_pantalla, text_string):
        textBitmap = self.font.render(text_string, True, NEGRO)
        mi_pantalla.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
    
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
    
    def indent(self):
        self.x += 10
    
    def unindent(self):
        self.x -= 10

# Inicializa pygame y la ventana
pygame.init()

# Establecemos el largo y alto de la pantalla
dimensiones = [500, 700]
pantalla = pygame.display.set_mode(dimensiones)
pygame.display.set_caption("Control de Joystick y Cámara")

# Inicializa el joystick
pygame.joystick.init()

# Para gestionar el refresco de pantalla
reloj = pygame.time.Clock()

# Para imprimir texto
text_print = TextPrint()

# Diccionario de nombres personalizados para los botones
nombres_botones = {
    0: "Botón X",
    2: "Botón Cuadrado",
    # Agrega otros botones si es necesario
}

# Variables para controlar la cámara
camara_abierta = False
cap = None
video_thread = None

def video_loop():
    global cap, camara_abierta
    while camara_abierta:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Real-Time Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

# Función para abrir la cámara
def abrir_camara():
    global cap, camara_abierta, video_thread
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se puede abrir la cámara")
    else:
        camara_abierta = True
        video_thread = threading.Thread(target=video_loop)
        video_thread.start()
        print("Cámara abierta")

# Función para cerrar la cámara
def cerrar_camara():
    global camara_abierta
    camara_abierta = False
    if video_thread is not None:
        video_thread.join()
    print("Cámara cerrada")

# Bucle principal del programa
hecho = False
while not hecho:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho = True
        
        # Verifica si un botón fue presionado para abrir la cámara
        if evento.type == pygame.JOYBUTTONDOWN:
            print(f"Botón presionado: {evento.button}")  # Agregar declaración de impresión
            # Si el botón Cuadrado (2) fue presionado, abrir la cámara
            if evento.button == 2 and not camara_abierta:
                abrir_camara()
            # Si el botón X (0) fue presionado, cerrar la cámara
            elif evento.button == 0 and camara_abierta:
                cerrar_camara()
    
    # Limpiamos la pantalla con color blanco
    pantalla.fill(BLANCO)
    text_print.reset()

    # Imprime el número de joysticks conectados
    joystick_count = pygame.joystick.get_count()
    text_print.print(pantalla, "Número de joysticks: {}".format(joystick_count))
    text_print.indent()

    # Para cada joystick
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        text_print.print(pantalla, "Joystick {}".format(i))
        text_print.indent()

        # Obtiene el número de botones y verifica si son presionados
        botones = joystick.get_numbuttons()
        text_print.print(pantalla, "Número de botones: {}".format(botones))
        text_print.indent()

        for i in range(botones):
            boton = joystick.get_button(i)
            nombre_boton = nombres_botones.get(i, f"Botón {i}")
            text_print.print(pantalla, "{} valor: {}".format(nombre_boton, boton))
        text_print.unindent()
        text_print.unindent()

    # Actualizamos la pantalla
    pygame.display.flip()

    # Limitamos a 60 fotogramas por segundo
    reloj.tick(60)

# Cerrar la cámara si está abierta
if camara_abierta:
    cerrar_camara()

pygame.quit()
