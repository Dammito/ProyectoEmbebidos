#Servidor
import os
import socket

from http.server import BaseHTTPRequestHandler, HTTPServer
from serial import *
from time import *

#modeloPlaga
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np




#base de datos
import pyrebase


#turtle
import turtle

#camara
#import os
#from picamera2 import *
import time

#camera = Picamera2()

#preview_config = camera.create_preview_configuration(main={"size": (800, 600)})
#camera.configure(preview_config)


# Carga el modelo
model = load_model('/home/pi/Documents/keras_model.h5')
info = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

#cargar base de datos
config = {
  "apiKey": "TuPNDg1qnwvBIrJgImUJMIY4b9pzZuXh6z0crxF2",
  "authDomain": "iotproyecto-164cf.firebaseapp.com",
  "databaseURL": "https://iotproyecto-164cf-default-rtdb.firebaseio.com/",
  "storageBucket": "iotproyecto-164cf.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
data = {
            "sector": "Sector1",
        }
db.child("Sector").set(data)




def sondeoPlaga():
  #os.system('libcamera-jpeg -o image.jpg')
  #camera.start()
  #camera.switch_mode_and_capture_file(capture_config,'/home/pi/Documents/image.jpg')
  #camera.capture('/home/pi/Documents/image.jpg')
  #camera.start()
  time.sleep(2)
  #camera.capture_file('/home/pi/Documents/image.jpg')

  #camera.close()
  
  image = Image.open('/home/pi/Documents/image.jpg') #ingresar la ruta actualizada de las imagenes
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.ANTIALIAS)
  image_array = np.asarray(image)
  normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
  info[0] = normalized_image_array
  prediction = model.predict(info)
  if prediction[0][0] > prediction[0][1]:
      data = {
        "prediccion": "nomilia", #"prediccion": prediccion,
      }
      db.child("Prediccion").set(data)
      print("nomilia")
  elif prediction[0][1] > prediction[0][0]:
      data = {
        "prediccion": "normal", #"prediccion": prediccion,
      }
      db.child("Prediccion").set(data)
      print("normal")
      
  
  

def sonicos():
  atmega.write("activarSonicos".encode())  # para recibir los datos de la funcion sonico
  sonico1 = atmega.readline().strip()
  sonico2 = atmega.readline().strip()
  sonico3 = atmega.readline().strip()
  sonico1 = sonico1.decode()
  sonico2 = sonico2.decode()
  sonico3 = sonico3.decode()
  atmega.readline().strip()
  sonico1 = float(sonico1) #derecha
  sonico2 = float(sonico2) #frente
  sonico3 = float(sonico3) #izquierda
  data = {
    "sonico1": sonico1,
    "sonico2": sonico2,
    "sonico3": sonico3,
  }
  db.child("Sonico").set(data)
  
  
def dhtsensor():
  atmega.write("activarTemp".encode())  # para recibir los datos de la funcion dht
  temperatura = atmega.readline().strip()
  humedad = atmega.readline().strip()
  atmega.readline().strip()
  temperatura = temperatura.decode()
  humedad = humedad.decode()
  data = {
    "temperatura": float(temperatura),
    "humedad": float(humedad),
  }
  db.child("Dht").set(data)


atmega = Serial('/dev/ttyACM0', 9600)
sleep(2)

#lista recorrido
global recorrido
recorrido = []
global recorridoRetorno
recorridoRetorno = []
#lista sector
global sectores
sectores = []
global sectoresRetorno
sectoresRetorno = []
global sector
sector = 1
global confRec
confRec = 0
  
def servidor():
  comando = None
    
  class RequestHandler_httpd(BaseHTTPRequestHandler):
    #confRec = 0
    
    def do_GET(self):      
      global confRec
      global sector
      global sectoresRetorno
      global sectores
      global recorridoRetorno
      global recorrido
      global comando
      messagetosend = bytes('Hola mundo',"utf")
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', len(messagetosend))
      self.end_headers()
      self.wfile.write(messagetosend)
      comando = self.requestline
      comando = comando[5 : int(len(comando)-9)]
      if comando == 'delante':
        atmega.write("delante".encode())
        atmega.readline().strip()
        if confRec == 1:
          #guardar datos recorrido
          recorrido.append("delante")
          recorridoRetorno.append("delante")
          sectores.append("Sector "+str(sector))
        sonicos()
        dhtsensor()
        #sondeoPlaga()
              
      elif comando == 'izquierda':
        atmega.write("izquierda".encode())
        atmega.readline().strip()
        if confRec == 1:
          #guardar datos recorrido
          recorrido.append("izquierda")
          recorridoRetorno.append("derecha")
          sectores.append("Sector "+str(sector))
        sonicos()
        dhtsensor()
              
      elif comando == 'atras':
        atmega.write("atras".encode())
        atmega.readline().strip()
        if confRec == 1:
          #guardar datos recorrido
          recorrido.append("atras")
          recorridoRetorno.append("atras")
          sectores.append("Sector "+str(sector))
        sonicos()
        dhtsensor()
              
      elif comando == 'derecha':
        atmega.write("derecha".encode())
        atmega.readline().strip()
        if confRec == 1:
          #guardar datos recorrido
          recorrido.append("derecha")
          recorridoRetorno.append("izquierda")
          sectores.append("Sector "+str(sector))
        sonicos()
        dhtsensor()
            
      elif comando == 'recorridoActivado':
        recorrido = []
        recorridoRetorno =  []
        confRec = 1
            
      elif comando == 'guardarRecorrido':
        confRec = 0
        sector = 1
        sectoresRetorno = list(reversed(sectores))
        recorridoRetorno = recorridoRetorno[::-1]
        print(recorrido) #solo para revisar
        print(recorridoRetorno)#solo para revisar
        #GIRO 180 GRADOS
        atmega.write("derecha".encode())
        atmega.readline().strip()
        atmega.write("derecha".encode())
        atmega.readline().strip()
        #inicio del retorno
        for i in recorridoRetorno:
          atmega.write(i.encode())
          atmega.readline().strip()
        #giro 180 grados
        atmega.write("derecha".encode())
        atmega.readline().strip()
        atmega.write("derecha".encode())
        atmega.readline().strip()
          
      elif comando == 'iniciarRecorrido':
        if confRec == 0:
          #recorrido
          con = 0
          for i in recorrido:
            atmega.write(i.encode())
            atmega.readline().strip()
            data = {
              "sector": sectores[con],
            }
            db.child("Sector").set(data)
            con+=con
          #giro 180 grados
          atmega.write("derecha".encode())
          atmega.readline().strip()
          atmega.write("derecha".encode())
          atmega.readline().strip()
          #recorrido retorno
          con = 0
          for j in recorridoRetorno:
            atmega.write(j.encode())
            atmega.readline().strip()
            data = {
              "sector": sectoresRetorno[con],
            }
            db.child("Sector").set(data)
            con+=con
          #giro 180 grados
          atmega.write("derecha".encode())
          atmega.readline().strip()
          atmega.write("derecha".encode())
          atmega.readline().strip()
          
      elif comando == 'nuevoSector':
        if confRec == 1:
          sector+=sector
          data = {
            "sector": "Sector"+str(sector),
          }
          db.child("Sector").set(data)
            
      elif comando == 'activarAutomatico':
        atmega.write("activarAutomatico".encode())
        atmega.readline().strip()
      
      elif comando == 'desactivarAutomatico':
        atmega.write("desactivarAutomatico".encode())
        atmega.readline().strip()
            
      atmega.write('\r'.encode())
  
      atmega.flushInput()
      sleep(0.3)

  server_address_httpd = ('192.168.100.102',8080) #Casa
  #server_address_httpd = ('10.10.0.17',8092)   #U
  httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
  print('Starting server.')
  httpd.serve_forever()
    


def main () :
  

# Infinite loop
 try:
   while 1 :
     servidor()
 except(KeyboardInterrupt,SystemExit):
   print("\nhasta la vista ")
   atmega.close()
# Command line execution
if __name__ == '__main__' :
   main()

    
    

