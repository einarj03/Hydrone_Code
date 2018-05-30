//Var For Speedmeter
volatile byte detect_nth_ping = 0;
// used to store fraction of revolution

unsigned long rpm = 0;
unsigned long lastrpmtime;
unsigned long lastlogtime;
//SD Card Paramters
#include <SD.h> 
#include <SPI.h>
#define LOG_INTERVAL 1000   // mills between entries (Reduce to take more/faster data)
#define SYNC_INTERVAL 1000 
uint32_t syncTime = 0;    // time of last sync ()
unsigned long timegap = 0;
unsigned int pings_per_rev = 6; //depends on break disk
unsigned int pings_per_log = 6;
unsigned int max_log_interval = 500;
unsigned int min_log_interval = 100;
const byte interruptPin = 2;

void setup()
{
  Serial.begin(9600);
  pinMode(interruptPin, INPUT_PULLUP);
//  digitalPinToInterrupt(interruptPin);
  attachInterrupt(0, wheel_detect, RISING);//Calls wheel_detect when pin 2 (or 2, 3, 18, 19, 20, 21 on mega or just 2,3 on uno)
  rpm = 0;
  lastrpmtime = 0;
  lastlogtime = 0;

}
void loop()//Measure RPM
{
  if (detect_nth_ping >= pings_per_log || millis() - lastrpmtime >= max_log_interval) { 
//    rpm = ((60*1000)/(millis() - lastrpmtime))*(detect_nth_ping/pings_per_rev);
//    String rpmstring = String(rpm);

    Serial.print(millis() - lastrpmtime);
    Serial.print(",");    
    Serial.print(analogRead(A0)); 
    Serial.print(",");
    Serial.print(analogRead(A1));
    Serial.print(",");
    Serial.print(detect_nth_ping);
    Serial.println();

    lastrpmtime = millis();
    detect_nth_ping = 0;

    if (millis()-lastlogtime < min_log_interval) {
      delay (min_log_interval - (millis() - lastlogtime));
    }
    
    lastlogtime = millis();
  }
}
void wheel_detect()//This function is called whenever a magnet/interrupt is detected by the arduino
{
     detect_nth_ping++;
//     Serial.println("detect");
}
