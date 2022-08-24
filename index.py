
import serial
import time
import eel
import json
from pySerialTransfer import pySerialTransfer as txfer
  
eel.init("frontend")  
  

arduino = serial.Serial(port='COM11', baudrate=115200, timeout=.1)


file = open("./test files/test.bin","rb")

hexData = file.read().hex()

file.close()

hexStringList =list(map(''.join, zip(*[iter(hexData)]*2)))

decList = []
writeLength=[]
writeLength.append(int(len(hexStringList)))
for hex_value in hexStringList:
            int_value = int(hex_value, base=16)
            decList.append(int_value)

time.sleep(2)

@eel.expose  
def getCommand(command):
                         
        
    if(command == "write" or command =="w"):
    
        arduino.write(bytes("C-WRITE", 'utf-8'))
        
        while arduino.inWaiting() == 0:
                time.sleep(0.01)
        returned_data = arduino.readline()
        
        arduino.write(bytearray(writeLength))
        arduino.write(bytearray(decList))
        while arduino.inWaiting() == 0:
            time.sleep(0.01)
        
        isWriting = True
        while isWriting == True:      
            time.sleep(0.01)
            returned_data = arduino.readline().decode('utf-8')
            
            if(returned_data == "WRITE-END"):
                
                
                returned_values = {
                    "dec":decList,
                    "hex":hexStringList
                    
                }
                isWriting == False
                return json.dumps(returned_values) 
            
       
    
                
    elif(command == "erase" or command =="e"):
        arduino.write(bytes("C-ERASE", 'utf-8'))
        
        while arduino.inWaiting() == 0:
                time.sleep(0.01)
        returned_data = arduino.readline()
      
        isErasing = True
        while isErasing ==True:
            time.sleep(0.01)
            returned_data = arduino.readline().decode('utf-8')
           
            if(returned_data == "ERASE-DONE"):
                isErasing = False
                returned_values = {"message":"Erase completed sucessfully"}
                print("done")
                return json.dumps(returned_values)
          
          
          
                    
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
                return json.dumps({"message":"READ FAILED"})
            if(returned_data ==" "):
                failedReads+1
            if(returned_data == "READ-DONE"):
                isReading = False
            
                
            hex_array.append(returned_data)
    
        returned_values = {"hex":hex_array}   
       
        return json.dumps(returned_values)    
     

eel.start("index.html")