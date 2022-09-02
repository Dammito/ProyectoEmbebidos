from http.server import BaseHTTPRequestHandler, HTTPServer
from serial import *
from time import *


def sonicos():
    atmega.write("activarSonicos".encode())  # para recibir los datos de la funcion sonico
    sonico1 = atmega.readline().strip()
    sonico2 = atmega.readline().strip()
    sonico3 = atmega.readline().strip()
    return sonico1,sonico2,sonico3

atmega = Serial('/dev/ttyACM0', 9600)
sleep(2)

sonAc = 0
comando = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global comando
    messagetosend = bytes('Hola mundo',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    comando = self.requestline
    comando = comando[5 : int(len(comando)-9)]
    print(comando)
    if comando:
        if comando == 'delante':
            atmega.write("delante".encode())
            if sonAc == 1:
                sonicos()
        elif comando == 'izquierda':
            atmega.write("izquierda".encode())
            if sonAc == 1:
                sonicos()
        elif comando == 'atras':
            atmega.write("atras".encode())
            if sonAc == 1:
                sonicos()
        elif comando == 'derecha':
            atmega.write("derecha".encode())
            if sonAc == 1:
                sonicos()
        elif comando == 'n':
            sonAc = 1
        elif comando == 'm':  # desactivar sonicos
            sonAc = 0
    atmega.write('\r'.encode())

    atmega.flushInput()
    sleep(0.3)

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
    return

except(KeyboardInterrupt, SystemExit):
    print("")
    print("hasta la vista ")
    atmega.close()

server_address_httpd = ('url1',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Starting server.')
httpd.serve_forever()
GPIO.cleanup()
