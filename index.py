
import serial
import time
import eel
import json
from random import randint
  
eel.init("frontend")  
  

arduino = serial.Serial(port='COM11', baudrate=115200, timeout=.1)

file = open("./test.bin","rb")

hexData = file.read().hex()
print(hexData)
file.close()

hexList =list( map(''.join, zip(*[iter(hexData)]*2)))
time.sleep(2)

@eel.expose  
def getCommand(command):
   
    if(command == "write" or command =="w"):
        dec_array=[]
        arduino.write(bytes("C-WRITE", 'utf-8'))
        while arduino.inWaiting() == 0:
                time.sleep(0.01)
        returned_data = arduino.readline()
        print(returned_data)
        for hex_value in hexList:
            int_value = str(int(hex_value, base=16))
            arduino.write(bytes(int_value, 'utf-8'))
            while arduino.inWaiting() == 0:
                time.sleep(0.01)
            time.sleep(0.01)
            returned_data = arduino.readline()
            print("HEX -- ",hex_value)
            print("DEC -- ",returned_data)
            if(returned_data != ""):
                dec_array.append(returned_data.decode('utf-8'))
        print(dec_array)
        print(hexList)  
        returned_values ={
            "dec":dec_array,
            "hex":hexList
            
        }
        dec_array =[]
        return json.dumps(returned_values)               
    elif(command == "erase" or command =="e"):
        arduino.write(bytes("C-ERASE", 'utf-8'))
        time.sleep(1)
        
    elif(command == "read" or command =="r"):
        hex_array=[]
        failedReads = 0
        isReading =True 
        arduino.write(bytes("C-READ", 'utf-8'))
        while arduino.inWaiting() == 0:
                time.sleep(0.01)
        while isReading == True:
            time.sleep(0.01)
            returned_data = arduino.readline().decode('utf-8')
            if(failedReads > 5):
                isReading =False
                return json.dumps({"error":"READ FAILED"})
            if(returned_data ==""):
                failedReads+1
            if(returned_data == "READ-DONE"):
                isReading = False
                
            hex_array.append(returned_data)
            print('ret-----',returned_data)
            
        returned_values = {"hex":hex_array}   
        print(returned_values)
        return json.dumps(returned_values)    
     

eel.start("index.html")