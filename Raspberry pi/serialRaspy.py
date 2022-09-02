from serial import *
from time import *


def sonicos():
    sonico1 = 0 #izquierda
    sonico2 = 0 #frente
    sonico3 = 0 #derecha
    if sonAc == 1:
        atmega.write("activarSonicos".encode())  # para recibir los datos de la funcion sonico
        sonico1 = atmega.readline().strip()
        sonico2 = atmega.readline().strip()
        sonico3 = atmega.readline().strip()
    return sonico1,sonico2,sonico3

atmega = Serial('/dev/ttyACM0', 9600)
sleep(2)

sonAc = 0

try:
    while 1:
        comando = input("""Seleccione entre las siguientes opciones:
        w = delante
	    a = izquierda
	    s = atras
	    d = derecha
	    n = activar sonicos
	    m = desactivar sonicos
	    k = activar deteccion
	    l = desactivar deteccion
	    su eleccion:.. """)
        if comando:
            if comando == 'w':
                atmega.write("delante".encode())
                sonicos()
            elif comando == 'a':
                atmega.write("izquierda".encode())
                sonicos()
            elif comando == 's':
                atmega.write("atras".encode())
                sonicos()
            elif comando == 'd':
                atmega.write("derecha".encode())
                sonicos()
            elif comando == 'n':
                sonAc = 1
            elif comando == 'm':  # desactivar sonicos
                sonAc = 0
        atmega.write('\r'.encode())

        atmega.flushInput()
        sleep(0.3)
        print(enviado)

        try:
            print("recibiendo datos: ")
            while not (atmega.in_waiting > 0):
                print("datos recibidos")
                sleep(1.5)
                pass
            print()
            mens = atmega.readline().strip()
            print(mens.decode())

        except:
            print("no data recive")


except(KeyboardInterrupt, SystemExit):
    print("")
    print("hasta la vista ")
    atmega.close()
