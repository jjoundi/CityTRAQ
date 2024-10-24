// TM1637 SevenSegment Counter Wokwi Example
//
// https://wokwi.com/projects/339227323398095442

#include <TM1637.h>

const int CLK = 2;
const int DIO = 3;

TM1637 tm(CLK, DIO);
unsigned int counter = 0;
int button=7;
int val=0;
int old_val=0;
int state=0;

void setup() {
  tm.init();
  tm.set(BRIGHT_TYPICAL);
  // put your setup code here, to run once:
  // instantiate pushbuttons
  // instantiate pins for LCD screen
}

void loop() {
  // put your main code here, to run repeatedly:
  // If button 1 is pressed increase Bike Counter with 1
  // If button 2 is pressed increase Pedestrian Counter with 1
  // If button 3 is pressed increase Car Counter with 1
  tm.display(0, (counter / 1000) % 10);
  tm.display(1, (counter / 100) % 10);
  tm.display(2, (counter / 10) % 10);
  tm.display(3, counter % 10);
  val=digitalRead(button);
  if( (val==HIGH) && (old_val==LOW)) 
  {
    state=1-state;
  }
  old_val=val;
  if (state==1) 
  { 
      counter++;
      state=1-state;
  }

}
