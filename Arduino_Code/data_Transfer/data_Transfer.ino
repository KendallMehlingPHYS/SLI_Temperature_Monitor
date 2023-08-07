int address1 = 7; //Address 0 for the MUX Chip (Maxim DG508A) 
int address2 = 6; //Address 1 for the MUX Chip
int address3 = 5; //Address 2 for the MUX Chip

int dataline = 1; // dataline will run from 1-8 and determine which of the sensors is connnected to the ADC. 

int analogPin = A3; // The connected sensor line that is connected to the ADC of the Arduino.

int val = 0;  // variable to store the value read
int samples = 1000; // How many samples to average over before sending over Voltage to Python.
int sum = 0;  // This will be the running tally of the ADC sum before transmission. 

void setup() {
  Serial.begin(9600);
}

void loop() {
  int dataline = 1;       // Simply begin with Sensor 1. If all digital address lines are LOW, ADC will read Sensor 1. 
  while(dataline <=8){    // Will run over all sensors. 
    const char* address = get_address(dataline);  
    set_mux(address);     // Sets MUX digital states.   
    int avg = get_avg();            // Gets average from the sensor. 
    Serial.print(address);
    Serial.print(" " );
    Serial.print(avg);
    dataline++;           // Move on to the next sensor. 
    delay(1000);          // Delay 1 second before moving to next sensor
  }
  delay(1000);          // Delay 10 seconds before reading sensor list again. 
 
}

int get_avg(){
  //Inputs: None. This function assumes the appropriate channel is closed on the MUX
  // and averages over the data before transmitting it to the Python plotter.  
  float sum = 0;
  for(int i = 0; i< samples; i++){
     val = analogRead(analogPin);
     sum += val;     
  }
  return sum/samples;
}

void set_mux(const char* address){
  // Inputs: const char* address. This function receives the binary representation of the dataline. This sets the digital state of 
  // the appropriate address pins on the MUX. 
  int state1 = int(address[0]);
  int state2 = int(address[1]);  
  int state3 = int(address[2]);

  digitalWrite(address1, state1);
  digitalWrite(address2, state2);
  digitalWrite(address3, state3);
  // At this point the MUX should have set up a new channel. We will then read the data and transmit it to Python for plotting. 
}

const char* get_address(int dataline){
  // Inputs: int dataline. This function simply returns the binary character representation of the dataline. This is brute force
  // But works for only 8 sensor lines. This will be used to close the appropriate address pins on for the MUX. 
  if(dataline == 1){
    return "000";
  }
  if(dataline == 2){
    return "001";
  }
    if(dataline == 1){
    return "000";
  }
  if(dataline == 3){
    return "010";
  }
    if(dataline == 4){
    return "011";
  }
  if(dataline == 5){
    return "100";
  }
    if(dataline == 6){
    return "101";
  }
  if(dataline == 7){
    return "110";
  }
    if(dataline == 8){
    return "111";
  }
}
