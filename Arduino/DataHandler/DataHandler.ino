//Var For Speedmeter
// used to store fraction of revolution
// include the LCD library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 13, 10, 8);

volatile byte detect_nth_ping = 0;

#define LOG_INTERVAL 1000   // mills between entries (Reduce to take more/faster data)
#define SYNC_INTERVAL 1000 

unsigned long rpm = 0;
unsigned long lastrpmtime;
unsigned long lastlogtime;

uint32_t syncTime = 0;    // time of last sync ()
unsigned long timegap = 0;
unsigned int pings_per_rev = 6; //depends on break disk
unsigned int pings_per_log = 6;
unsigned int max_log_interval = 500;
unsigned int min_log_interval = 100;
const byte interruptPin = 2;

unsigned long highPressure = 0;
unsigned long lowPressure = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(interruptPin, INPUT_PULLUP);
//  digitalPinToInterrupt(interruptPin);
  attachInterrupt(0, wheel_detect, RISING);//Calls wheel_detect when pin 2 (or 2, 3, 18, 19, 20, 21 on mega or just 2,3 on uno)
  rpm = 0;
  lastrpmtime = 0;
  lastlogtime = 0;

// set up the LCD's number of columns and rows:
  lcd.begin(16, 2);

  lcd.print("LCD Activated");
  delay(3000);
  lcd.clear();

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
    Serial.print(",");
    Serial.print(highPressure);
    Serial.print(",");
    Serial.print(lowPressure);
    Serial.println();

    lastrpmtime = millis();
    detect_nth_ping = 0;

    if (millis()-lastlogtime < min_log_interval) {
      delay (min_log_interval - (millis() - lastlogtime));
    }
    
    lastlogtime = millis();

    
  }
//  LCD is first cleared of earlier messages
  lcd.clear(); 

//  tells the LCD to start writing from column 0, row 0
  lcd.setCursor(0, 0);   

//  prints high pressure to the LCD 
  lcd.print("HP: ");
  lcd.print(highPressure);
  lcd.print("bar");  

// set the cursor to column 0, line 1
  lcd.setCursor(0, 1);

//  prints low pressure to the LCD
  lcd.print("LP: ");
  lcd.print(lowPressure);
  lcd.print("bar");
  
}
void wheel_detect()//This function is called whenever a magnet/interrupt is detected by the arduino
{
     detect_nth_ping++;
//     Serial.println("detect");
}
