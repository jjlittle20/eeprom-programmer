
import serial
import time

arduino = serial.Serial(port='COM11', baudrate=115200, timeout=.1)

file = open("./test.bin","rb")

hexData = file.read().hex()
print(hexData)
file.close()

hexList = map(''.join, zip(*[iter(hexData)]*2))
time.sleep(2)
command = input("READY -")
print(arduino)
def getCommand(command):
    if(command == "write" or command =="w"):
        arduino.write(bytes("C-WRITE", 'utf-8'))
        while arduino.inWaiting() == 0:
                time.sleep(0.1)
        returned_data = arduino.readline()
        print(returned_data)
        for hex_value in hexList:
            int_value = str(int(hex_value, base=16))
            arduino.write(bytes(int_value, 'utf-8'))
            while arduino.inWaiting() == 0:
                time.sleep(0.1)
            time.sleep(0.05)
            returned_data = arduino.readline()
            print("HEX -- ",hex_value)
            print("DEC -- ",returned_data)
            
         
    elif(command == "erase" or command =="e"):
        arduino.write(bytes("C-ERASE\n", 'utf-8'))
        time.sleep(1)
        
    elif(command == "read" or command =="r"):
        arduino.write(bytes("C-READ\n", 'utf-8'))
        time.sleep(1)

getCommand(command)
