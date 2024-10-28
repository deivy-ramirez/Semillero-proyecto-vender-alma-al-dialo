import RPi.GPIO as GPIO
import time
import pygame

# Configuración del servomotor
SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500
Servo = 23

def map(value, inMin, inMax, outMin, outMax):
    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin

def setup():
    global p
    GPIO.setmode(GPIO.BCM)       
    GPIO.setup(Servo, GPIO.OUT)  
    GPIO.output(Servo, GPIO.LOW) 
    p = GPIO.PWM(Servo, 50)     
    p.start(0)                    

def setAngle(angle):      
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)

def destroy():
    p.stop()
    GPIO.cleanup()

# Configuración del joystick
pygame.init()
pygame.joystick.init()
umbral_boton = 0.5

def main():
    setup()
    hecho = False
    reloj = pygame.time.Clock()

    while not hecho:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True

        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            # Obtener los valores de los ejes L2 y R2
            eje_l2 = joystick.get_axis(4)  # L2
            eje_r2 = joystick.get_axis(5)  # R2
            
            # Mapear los valores de los ejes a un rango de ángulos
            angle_l2 = map(eje_l2, -1, 1, 0, 180)  # Asumiendo que el eje va de -1 a 1
            angle_r2 = map(eje_r2, -1, 1, 0, 180)  # Asumiendo que el eje va de -1 a 1
            
            # Establecer el ángulo del servomotor basado en L2
            setAngle(angle_l2)

            # Puedes usar R2 para otro propósito o también para controlar el servomotor
            # setAngle(angle_r2)  # Descomentar si deseas usar R2

        # Actualiza la pantalla y limita la tasa de refresco
        pygame.display.flip()
        reloj.tick(60)

    destroy()
    pygame.quit()

if __name__ == '__main__':
    main()