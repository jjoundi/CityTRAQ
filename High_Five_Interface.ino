//Simulation
//https://wokwi.com/projects/412616408766429185

#include <TM1637.h>

const int CLK1 = 2;
const int DIO1 = 3;

const int CLK2 = 4;
const int DIO2 = 5;

const int CLK3 = 6;
const int DIO3 = 7;

TM1637 tm1(CLK1, DIO1);
TM1637 tm2(CLK2, DIO2);
TM1637 tm3(CLK3, DIO3);

unsigned int counter1 = 0;
unsigned int counter2 = 0;
unsigned int counter3 = 0;
int button1=8;
int button2=9;
int button3=10;
int val1=0; // ontdubbelen 
int old_val1=0; // ontdubbelen
int state1=0; // ontdubbelen

int val2=0; // ontdubbelen 
int old_val2=0; // ontdubbelen
int state2=0; // ontdubbelen

int val3=0; // ontdubbelen 
int old_val3=0; // ontdubbelen
int state3=0; // ontdubbelen

void setup() {
  //screen1
  tm1.init();
  tm1.set(BRIGHT_TYPICAL);
  //screen2
  tm2.init();
  tm2.set(BRIGHT_TYPICAL);
  //screen3
  tm3.init();
  tm3.set(BRIGHT_TYPICAL);
  // put your setup code here, to run once:
  // instantiate pushbuttons
  pinMode(button1, INPUT);
  pinMode(button2, INPUT);
  pinMode(button3, INPUT);
  // instantiate pins for LCD screen
}

void loop() {
  // put your main code here, to run repeatedly:
  // If button 1 is pressed increase Bike Counter with 1
  // If button 2 is pressed increase Pedestrian Counter with 1
  // If button 3 is pressed increase Car Counter with 1
  tm1.display(0, (counter1 / 1000) % 10);
  tm1.display(1, (counter1 / 100) % 10);
  tm1.display(2, (counter1 / 10) % 10);
  tm1.display(3, counter1 % 10);
  val1=digitalRead(button1);
  if( (val1==HIGH) && (old_val1==LOW)) 
  {
    state1=1-state1;
  }
  old_val1=val1;
  if (state1==1) 
  { 
      counter1++;
      state1=1-state1;
  }

  //screen 2
  // put your main code here, to run repeatedly:
  // If button 1 is pressed increase Bike Counter with 1
  // If button 2 is pressed increase Pedestrian Counter with 1
  // If button 3 is pressed increase Car Counter with 1
  tm2.display(0, (counter2 / 1000) % 10);
  tm2.display(1, (counter2 / 100) % 10);
  tm2.display(2, (counter2 / 10) % 10);
  tm2.display(3, counter2 % 10);
  val2=digitalRead(button2);
  if( (val2==HIGH) && (old_val2==LOW)) 
  {
    state2=1-state2;
  }
  old_val2=val2;
  if (state2==1) 
  { 
      counter2++;
      state2=1-state2;
  }

  //screen 3
  // put your main code here, to run repeatedly:
  // If button 1 is pressed increase Bike Counter with 1
  // If button 2 is pressed increase Pedestrian Counter with 1
  // If button 3 is pressed increase Car Counter with 1
  tm3.display(0, (counter3 / 1000) % 10);
  tm3.display(1, (counter3 / 100) % 10);
  tm3.display(2, (counter3 / 10) % 10);
  tm3.display(3, counter3 % 10);
  val3=digitalRead(button3);
  if( (val3==HIGH) && (old_val3==LOW)) 
  {
    state3=1-state3;
  }
  old_val3=val3;
  if (state3==1) 
  { 
      counter3++;
      state3=1-state3;
  }

}

