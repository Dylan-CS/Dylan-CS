#include <Adafruit_NeoPixel.h>
#include <Servo.h>      
#include "SevenSegmentTM1637.h" 
#include "dht.h"
#include <LiquidCrystal_I2C.h>
//#include "IRremote.h"
#include <Adafruit_Fingerprint.h>
#include "DFPlayer_Mini_Mp3.h"

//用了 0 1 2 3 4 5 6 7 8 9 10 12 13  A1 A2 A3
#define PIN_CLK        0       // CLK -pin0
#define PIN_DIO        1       // DIO -pin1
#define Key_Pin        2       // button's output -pin2
#define servoPin3      3       // house door steering gear -pin3
#define Ir_door        4       // human sensor-pin4
#define servoPin       5       // Garage door steering gear control- pin5
#define servoPin2      6       // Windows steering gear contro -pin6
#define DHT11_PIN      7       // DHT LCD -PIN 7
#define beep           8       // beep signal -pin8
#define fan            9       // fan =pin9
#define LED_Pin        10      // LED -pin10
#define finger_Pin     11      // fingerprint -pin11
#define IrPin          12      // infrared sensor -pin12 
#define LED_Y          13      // LED Green -pin13
#define Rain           A1      // Raindrop sensor output- pinA1
#define Smoke          A2      // smoke alarm output -pinA2
#define RECV_PIN       A3      // Infrared remote control input 

uint8_t   id = 1;             //fingerprint ID
#define   OpenAngle      120  //garage door
#define   CloseAngle     30   //garage door
#define   PIXEL_COUNT    8    //LED number
#define   OpenAngle2     135  //window
#define   CloseAngle2    45   //window
#define   OpenAngle3     0   //door
#define   CloseAngle3    90    //door
int Ligh;
int Rai;
int Smok;
int Humi;
int Temp;
int a[8]={0};

// SevenSegmentTM1637    display(PIN_CLK, PIN_DIO);
Adafruit_NeoPixel pixels(PIXEL_COUNT, LED_Pin, NEO_GRB + NEO_KHZ800);
LiquidCrystal_I2C lcd(0x27,20,4);   
dht DHT; 
//IRrecv irrecv(RECV_PIN); //Initializes an infrared receiver
//decode_results results; //Infrared received data variables
//Adafruit_Fingerprint finger = Adafruit_Fingerprint(&Serial);

void setup() { 
  // Set serial port baud rate 
  Serial.begin(9600);    
  IO_Init();
  Lcd_Init(); //LCD screen initialization
  //display.begin();   //Initialize the nixie tube
  //display.setBacklight(100);  
  pixels.begin();           
  pixels.show();
}

void loop() {
  lcd.clear();
  Data_Read();
  Dht11_Display();
  opencardoor();
  rainwin();
  beepfunction();
  HumidityFan();
  HumanSensor(); 
  smokealarm();
  
}

void IO_Init()
{
  pinMode(LED_Y, OUTPUT);
  pinMode(servoPin, OUTPUT);
  pinMode(servoPin2, OUTPUT);
  pinMode(servoPin3, OUTPUT);
  pinMode(Key_Pin, INPUT);
  pinMode(beep, OUTPUT);
  pinMode(fan, OUTPUT);
  pinMode(LED_Pin, OUTPUT);   
  digitalWrite(LED_Y, LOW);  
  servopulse(CloseAngle);
  servopulse_window(CloseAngle2);
  servopulse_door(CloseAngle3);
  digitalWrite(fan, HIGH);
  digitalWrite(LED_Pin, LOW);
  digitalWrite(beep,HIGH);
}

void Lcd_Init()
{
  lcd.init();                    
  lcd.backlight();
  lcd.setCursor(1,0);
  lcd.print("Welcome Home!");
  delay(1000);
  lcd.clear();
}

void beepfunction(){
   //Trigger buzzer
  int buttonState = digitalRead(Key_Pin);  
  //control beep through the state of button
  if(buttonState == 1){
    //beep work
    digitalWrite(beep, LOW);
    }
  else 
     digitalWrite(beep, HIGH);
}

void HumanSensor(){
  int buttonState = digitalRead(Ir_door); 
  //Determine whether the human body sensor detects people, if it detects people, turn on the light
  if(buttonState == 1){
    for(int i=0;i<8;i++){
      pixels.setPixelColor(i, pixels.Color(127,   127,   127));    //make the light on in RGB form
    } 
    servopulse_door(OpenAngle3);
    pixels.show();  
    }
  else {
    for(int i=0;i<8;i++){
      pixels.setPixelColor(i, pixels.Color(0,   0,   0));    //make the light off in RGB form 
    }  
    servopulse_door(CloseAngle3);   
    pixels.show();  
  }
}

void servopulse(int angle){
  for (int i = 0; i < 50; i++) {
         //Convert the angle into a pulse width value of 500-2480, every 1 degree more rotation, the corresponding high level is 11us more
         int pulsewidth=(angle*11)+500;  
         digitalWrite(servoPin,HIGH); 
         //The number of microseconds of the delay pulse width value
         delayMicroseconds(pulsewidth);  
         digitalWrite(servoPin,LOW);     
         delayMicroseconds(20000-pulsewidth);    
     }   
}

void servopulse_door(int angle){
  for (int i = 0; i < 50; i++) {
    // Convert the angle to a pulse width value of 500-2480, each additional degree of rotation corresponds to 11us more high level
         int pulsewidth=(angle*11)+500;  
         digitalWrite(servoPin3,HIGH);
          // microseconds of delay pulse width value
         delayMicroseconds(pulsewidth);  
         digitalWrite(servoPin3,LOW);     
         delayMicroseconds(20000-pulsewidth);    
     }   
}

void servopulse_window(int angle){
  for (int i = 0; i < 50; i++) {
    // Convert the angle to a pulse width value of 500-2480,
    //each additional degree of rotation corresponds to 11us more high level
         int pulsewidth=(angle*11)+500;  
         digitalWrite(servoPin2,HIGH);  
          // microseconds of delay pulse width value 
         delayMicroseconds(pulsewidth); 
         digitalWrite(servoPin2,LOW);     
         delayMicroseconds(20000-pulsewidth);    
     }   
}

void opencardoor(){
  if(digitalRead(IrPin)==0){
    //myservo.write(OpenAngle);    // Control the steering gear to turn and open the garage door
    servopulse(OpenAngle);
    digitalWrite(LED_Y, HIGH);    //Turn on the green light 
    delay(5000);  
    servopulse(CloseAngle);
    //myservo.write(CloseAngle);   //Control the steering gear to turn and close the garage door
    digitalWrite(LED_Y, LOW);    //Turn off the green light
  }
}

void rainwin(){
  if(Rai > 800){
   servopulse_window(CloseAngle2);   //close the window
  }
  else{
   servopulse_window(OpenAngle2);    //open the window
  }
}

/*
void light(){
  display.clear();
  display.print(1000-analogRead(A0));  //Digital tube displays light value through A0 pin
  delay(1000); 
}
*/

void smokealarm(){
  int smoketest = analogRead(Smoke);
  Serial.println(smoketest);
  if(Smok > 600){
   digitalWrite(beep, LOW);  //The buzzer beeps
  }
  else{
    digitalWrite(beep, HIGH);  //close the buzzer
  }
}

void HumidityFan(){ 
  //dht11 detects Temperature and Humidity Information     
  if(Humi < 90){
    digitalWrite(fan, HIGH);
    } 
  else{
    digitalWrite(fan, LOW);
    }
}

void Data_Read(){
  Ligh=0;
  Rai=0;
  Smok=0;
  Humi=0;
  DHT.read11(DHT11_PIN);
  Ligh = 1000-analogRead(A0);
  Rai  = analogRead(Rain);
  Smok = analogRead(Smoke);
  Temp  = DHT.temperature,1;
  Humi  = DHT.humidity,1;
}

void Dht11_Display()
{
  lcd.setCursor(0,0);
  lcd.print("T");
  lcd.print(":");
  toshow(Temp);
  //lcd.print(Temp);
  lcd.setCursor(8,0);
  lcd.print("H");
  lcd.print(":");
  toshow(Humi);
  //lcd.print(Humi);
  lcd.setCursor(0,1);
  lcd.print("L");
  lcd.print(":");
  toshow(Ligh);
  //lcd.print(Ligh);
  lcd.setCursor(8,1);
  
  lcd.print("R");
  lcd.print(":");
  toshow(Rai);
  //lcd.print(Rai-800);   
  delay(2000);
}

/*
void toshow(int n){
  int i=0;
  int a[5];
  for(int k=0;k++;k<=4){
    a[k]=0;
  }
  while(n!=0){
    a[i]=n%10;
    n=n/10;
    i=i+1;
  }  
  for(int j=4;j--;j>=0){
    if(a[j]!=0)
      lcd.print(a[j]);
  }
}
*/

void toshow(int n){
    int a,b;
    a=n;
    b=1;
    while(a>9){
    a/=10;
    b*=10;
    }
    //This while loop is used to count the number of bits of n, i.e., by b
    while(b>0){
    lcd.print(n/b);
    // Print 1 2 3 4 5 6 directly from the high position in order
    //printf("%d ",n/b);
    n%=b;
    b/=10;    
    }
}
