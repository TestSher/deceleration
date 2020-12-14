//2/12/2020
//╔═════════════════════════════════════════════════╗
//║"Wire.h" This library allows you to communicate with I2C devices (mpu6050)      ║                                                
//║<MPU6050_light.h> The mpu6050 library                                           ║                                                 
//║<LiquidCrystal.h> The library of the LCD display                                ║                                                 
//║                                                                                ║
//║setting a variable named timer(will be used in our raspberry to arduino com')   ║                                                 
//║lcd screen connections on the arduino 2-rs , 3-E  , 4-D4 , 5-D5 , 6-D6 , 7-D7   ║
//╚═════════════════════════════════════════════════╝                                                  

#include "Wire.h"                                   
#include <MPU6050_light.h>                          
#include <LiquidCrystal.h>                          
MPU6050 mpu(Wire);                                  
long timer = 0;                                     
LiquidCrystal lcd = LiquidCrystal(2, 3, 4, 5, 6, 7);
//char storedData[10];
//int Timer;

//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

//╔═════════════════════════════════════════════════╗
//║the I2C address of the board                                                    ║
//║writing to address 26(0x1A) of the register                                     ║
//║the options here are 0x00 which is off, and 0x01, 0x02, 0x03, 0x04, 0x05, 0x06  ║
//║0x06 being the highest filter setting                                           ║
//╚═════════════════════════════════════════════════╝

void InitMpu()
{                                                   
  Wire.beginTransmission(0x68);                                              
  Wire.write(0x1A);                                 
  Wire.write(0x06);                                 
  Wire.endTransmission(true);                      
  mpu.begin();                                      
}

//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

//╔═════════════════════════════════════════════════╗   
//║                                                                                ║
//║                 Prints the first message on the  lcd                           ║
//║                         while booting up                                       ║
//║                                                                                ║
//║                                                                                ║
//╚═════════════════════════════════════════════════╝
void FirstLCDmessage()
{                                                   
  lcd.setCursor(0, 0);                              
  lcd.print("Matmon");                              
  lcd.setCursor(0, 1);                              
  lcd.print("5000");                                 
}                                                   

//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

//╔═════════════════════════════════════════════════╗   
//║Sending the X acceleration value via the serial communication                   ║
//║                                                                                ║
//║Sending the Y acceleration value via the serial communication                   ║
//║                                                                                ║
//║Sending the Z acceleration value via the serial communication                   ║
//╚═════════════════════════════════════════════════╝
void printData()
{                                                                                            
    lcd.setCursor(0, 0);
    lcd.print("X=");
    lcd.setCursor(3, 0);
    lcd.print((mpu.getAccX())*9.82);
    lcd.setCursor(7, 0);
    lcd.print("m/s^2");
    lcd.setCursor(0, 1);
    lcd.print("Y=");
    lcd.setCursor(3, 1);
    lcd.print((mpu.getAccY())*9.82);
    lcd.setCursor(7, 1);
    lcd.print("m/s^2");
    
    Serial.print("#");
    Serial.print(mpu.getAccX());             
    Serial.print(",");                             
    Serial.print(mpu.getAccY());             
    Serial.print(",");                             
    Serial.print(mpu.getAccZ());             
    Serial.print("$\n");
    //Serial.print("\n");                             
    timer = millis();                               
    // end printData                                
}

//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

//╔═════════════════════════════════════════════════╗
//║                                                                                ║
//║                                                                                ║
//║wire.begin() - Initiating the Wire library and join the I2C bus                 ║
//║                                                                                ║
//║                                                                                ║
//╚═════════════════════════════════════════════════╝

void setup() 
{                                                   
  InitMpu();                                        
  lcd.begin(16, 2);                                 
  FirstLCDmessage();                                
  Wire.begin();                                      
  delay(1000);                                      
  lcd.begin(16,2);                                  
  Serial.begin(9600);                               
  Serial.print(F("X(m/s^2)  Y(m/s^2)  Z(m/s^2)\n"));
}                                                   

//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

//╔═════════════════════════════════════════════════╗
//║                                                                                ║
//║  recieving a  number between 0-999 from the raspberry pi                       ║
//║  the number is used to determine the delta between each measurement            ║
//║                                                                                ║
//║                                                                                ║
//╚═════════════════════════════════════════════════╝

/*long GetRaspberryMsg()
{
  if( Serial.available() )
  { 
    int i=0;
   while(Serial.available())          
    {
      char inChar = Serial.read();
     storedData[i++] += inChar;
    }
  }
if(storedData[0]=='#'||storedData[1]=='t'){Timer=(storedData[2]-0x30)*100+(storedData[3]-0x30)*10+(storedData[4]-0x30);} //char
}*/

//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

//╔═════════════════════════════════════════════════╗
//║                                                                                ║
//║ mpu.update() calls to a function from the library to update the measruements   ║
//║                                                                                ║
//║ printData() calls the print data function                                      ║
//║                                                                                ║
//║                                                                                ║
//╚═════════════════════════════════════════════════╝

void loop() {
  mpu.update();
  //GetRaspberryMsg();
  if(millis() - timer > 100) //REFRESH RATE ms
//  if(millis() - timer > Timer) //REFRESH RATE ms
 {
   printData();
 }
}
 
//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -








//██╗░░░██╗░█████╗░██████╗░░█████╗░███╗░░██╗  ░██████╗██╗░░██╗███████╗██████╗░
//╚██╗░██╔╝██╔══██╗██╔══██╗██╔══██╗████╗░██║  ██╔════╝██║░░██║██╔════╝██╔══██╗
//░╚████╔╝░███████║██████╔╝██║░░██║██╔██╗██║  ╚█████╗░███████║█████╗░░██████╔╝
//░░╚██╔╝░░██╔══██║██╔══██╗██║░░██║██║╚████║  ░╚═══██╗██╔══██║██╔══╝░░██╔══██╗
//░░░██║░░░██║░░██║██║░░██║╚█████╔╝██║░╚███║  ██████╔╝██║░░██║███████╗██║░░██║
//░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝  ╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
