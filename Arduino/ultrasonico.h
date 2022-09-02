#define __DELAY_BACKWARD_COMPATIBLE__

#include <stdbool.h>
#include <stdlib.h>
#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>
//#define F_CPU 16000000
float tifinal=0,duracion;
//FUNCIONES

char rec1[20] ;

void eccho(int pin_trigger, int pin_echo){
	while(!(PIND&(1<<pin_echo)));//esperar mientras no reciba el eco
	TCNT1 = 0;	//contador en cero
	TCCR1B = 0B101; //PREESCALADOR DE 1024 y se activa el contador
	while((PIND&(1<<pin_echo)) && TCNT1 < 500);//esperar mientras el eco esta en alto
	TCCR1B &= ~(1<<0) & ~(1<<2);//(1 << WGM12);//desactivar el contador
	tifinal = TCNT1;	//valor del contador
	duracion = tifinal; 	
	_delay_us(10);
}

void trigger(int pin_trigger, int pin_echo){
	PORTD |=(1<<pin_trigger); //trig high
	_delay_us(10);
    PORTD &=~ (1<<pin_trigger); //trig low
	eccho(pin_trigger, pin_echo);
}


int ultra(int pin_trigger, int pin_echo){
DDRD |= (1<<pin_trigger); //SALIDA PINES PD5(OC0B) Y PD6(OC0A)
DDRD &= ~(1<<pin_echo);
 trigger(pin_trigger, pin_echo);	
 return duracion;
}