#define SHIFT_DATA 2
#define SHIFT_CLK 3
#define SHIFT_LATCH 4
#define EEPROM_D0 5
#define EEPROM_D7 12
#define WRITE_EN 13


String COMMAND = "NO-OP";

int address = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(SHIFT_DATA, OUTPUT);
  pinMode(SHIFT_CLK, OUTPUT);
  pinMode(SHIFT_LATCH, OUTPUT);
  digitalWrite(WRITE_EN, HIGH);
  pinMode(WRITE_EN, OUTPUT);
  Serial.begin(115200);
  //  Serial.setTimeout(1);

  //  // Erase entire EEPROM
  //  Serial.print("Erasing EEPROM");
  //  for (int address = 0; address <= 2047; address += 1) {
  //    writeEEPROM(address, 0xff);
  //
  //    if (address % 64 == 0) {
  //      Serial.print(".");
  //    }
  //  }
  //  Serial.println(" done");


  //  // Read and print out the contents of the EERPROM
  //  Serial.println("Reading EEPROM");
  //  printContents();
//  Serial.print("READY---");
}

void setAddress(int address, bool outputEnable) {
  shiftOut(SHIFT_DATA, SHIFT_CLK, MSBFIRST, (address >> 8) | (outputEnable ? 0x00 : 0x80));
  shiftOut(SHIFT_DATA, SHIFT_CLK, MSBFIRST, address);

  digitalWrite(SHIFT_LATCH, LOW);
  digitalWrite(SHIFT_LATCH, HIGH);
  digitalWrite(SHIFT_LATCH, LOW);
}


void loop() {

  if (Serial.available() > 0 && COMMAND == "C-WRITE\n") {
    for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
      pinMode(pin, OUTPUT);
    }
    String dataString = Serial.readString();
    int dataInt = dataString.toInt();
    Serial.print(dataInt);
    setAddress(address, /*outputEnable*/ false);
    for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
      digitalWrite(pin, dataInt & 1);
      dataInt = dataInt >> 1;
    }
    digitalWrite(WRITE_EN, LOW);
    delayMicroseconds(1);
    digitalWrite(WRITE_EN, HIGH);
    delay(10);
    address++;
  }
  else if (Serial.available() > 0 && COMMAND == "NO-OP") {
    String data = Serial.readString();

    if (data.charAt(0) == 'C') {
      COMMAND = data;
      Serial.print(COMMAND);
    }
  }
  else if(Serial.available() > 0){
    String data = Serial.readString();
    Serial.print(data);
    }
  
}
