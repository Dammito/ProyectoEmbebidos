#include <Arduino.h>
#include <avr/io.h>
#include <util/delay.h>
#include <stdbool.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include "ultrasonico.h"


#define PRO_CPU 0
#define APP_CPU 1


//L298N control pins
int motorB2 = PB3;
int motorB1 = PB2;
int motorA2= PB1;
int motorA1 = PB0;

bool confDelante = false;

char charVal1[10]; //valores string ultrasonico 1
char charVal2[10]; //valores string ultrasonico 2
char charVal3[10]; //valores string ultrasonico 3

String lect; //lectura del serial

//sensor pins
DHT dht(A0, DHT11);



//Definir funciones
void movimientoAlto();
void movimientoDelante();
void movimientoAtras();
void giroDerecha();
void giroIzquierda();
void ultrasonicos();
void dhtSensor();

//automatico
int automatico = 0;
float sonico1 = 0;
float sonico2 = 0;
float sonico3 = 0;


void setup()
{
	DDRC |= 0b1;
	DDRB |= 0b1111;
	DDRD |= 0b11111100;

	Serial.begin(9600);   // Inicializamos  el puerto serie 
	dht.begin();  //Inicializamos el puert dht
	delay(3000);
}
void loop()
{
	lect = "";
	if(Serial.available()>0)    // Si llega un dato por el puerto BT se envía al monitor serial
	{
		lect = Serial.readStringUntil('\r');
		
	}


	if (lect == "delante") {
    if (automatico == 0){
      movimientoDelante();
		  delay(250);
		  movimientoAlto();
    }
		Serial.println("movimiento delante.") ;
	}
  	else if (lect == "atras") {
		movimientoAtras();
		delay(250);
		movimientoAlto();
		Serial.println("movimiento atras.") ;
	}
	else if (lect == "derecha") {
		giroDerecha();
		delay(250);
		movimientoAlto();
		Serial.println("movimiento derecha.") ;
	}
	else if (lect == "izquierda") {
		giroIzquierda();
		delay(250);
		movimientoAlto();
		Serial.println("movimiento izquierda.") ;
	}
	else if (lect == "activarSonicos"){
		ultrasonicos();
		Serial.println("Sonicos activados.") ;
	}
	else if (lect == "activarTemp"){
		dhtSensor();
		Serial.println("Temp enviados.") ;
	}

  else if (lect == "activarAutomatico"){
    automatico = 1;
		Serial.println("automaticoActivado.") ;
	}
  
  else if (lect == "desactivarAutomatico"){
    automatico = 0;
		Serial.println("automaticoDesactivado.") ;
	}

  if(automatico == 1){
    //Sonico 1
    sonico1 = ultra(3,2);
    //Sonico 2
    sonico2 = ultra(3,2);
    //Sonico 3
    sonico3 = ultra(3,2);

    if(sonico2<=50)
    {          
      if(sonico1>sonico3)  
      {
        if((sonico1<=30)&&(sonico3<=30))
       {movimientoAlto();
      delay(200);
        movimientoAtras();
        delay(1000);
       
       }
      else{
        giroDerecha();
        delay(500);}
        
      }
       else if(sonico1<sonico3)
       { 
        if((sonico1<=30)&&(sonico3<=30))
       
       {movimientoAlto();
      delay(200);
        movimientoAtras();
        delay(500);
       }
       else{
        giroIzquierda();
        delay(500);
       }
    }  
    }
    else if(sonico1<=15)
    {
      giroIzquierda();
      delay(500);
    }
    
    else if(sonico3<=15)
    {
      giroDerecha();
      delay(500);
    }
    else{
        movimientoDelante();
        }
  }


	delay(250);
}

//MOVIMIENTOS CARRO
void movimientoAlto(){
	PORTB = 0b0;
	//PORTB = ~(1<<motorA1) & ~(1<<motorA2) & ~(1<<motorB1) & ~(1<<motorB2);
}

void movimientoDelante(){
  PORTB = 0b1010;
	//PORTB &= ~(1<<motorA1) & (1<<motorA2) & ~(1<<motorB1) & (1<<motorB2);
}

void movimientoAtras(){
	PORTB = 0b0101;
	//PORTB = (1<<motorA1) & ~(1<<motorA2) & (1<<motorB1) & ~(1<<motorB2);
}

void giroDerecha(){
	PORTB = 0b1001;
	//PORTB &= (1<<motorA1) & ~(1<<motorA2) & ~(1<<motorB1) & (1<<motorB2);
}

void giroIzquierda(){
	
  PORTB = 0b0110;
	//PORTB &= ~(1<<motorA1) & (1<<motorA2) & (1<<motorB1) & ~(1<<motorB2);
}

//ULTRASONICOS
void ultrasonicos(){
	//Sonico 1
	dtostrf(ultra(3,2), 2, 4, charVal1); // pin_trigger 3, pin_echo 2 derecho
	Serial.println(charVal1);
	//Sonico 2
	dtostrf(ultra(5,4), 2, 4, charVal2); // pin_trigger 5, pin_echo 4 medio
	Serial.println(charVal2);
	//Sonico 3
	dtostrf(ultra(7,6), 2, 4, charVal3); // pin_trigger 7, pin_echo 6 izquierdo
	Serial.println(charVal3);
}

//SENSOR HUMEDAD TEMPERATURA
void dhtSensor(){
	Serial.println(dht.readTemperature()*10); // Obtener temperatura en C
	Serial.println(dht.readHumidity()); // Obtener temperatura en C
}