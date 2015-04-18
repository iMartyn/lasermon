import serial
import json
import csv

log = open('debug.log','a')
csvfile = open('cuts.csv', 'a')
try:
    usage = open('usage.json', 'r');
    usageJson = usage.read()
    usage.close()
except:
    usageJson = ""

if (usageJson == ""):
    usageObject = {'totalTime': 0, 'userTime': {}, 'laserState': 0}
else:
    usageObject = json.loads(usageJson)

ser = serial.Serial('/dev/ttyACM0',9600,timeout=10)
print("Serial open\n");
while 1:
    line = ser.readline()
    log.write(line.rstrip('\r\n')+"\n")
    print(line.rstrip('\r\n')+"\n")
    if (line == "RDY?\r\n"):
        ser.write("Y\n")
        usageObject['laserState'] = 1
        usage = open('usage.json', 'w')
        usage.write(json.dumps(usageObject))
        usage.close()
    if (line == 'CardGONE\r\n'):
        usageObject['laserState'] = 0
        csvline = ser.readline().rstrip('\r\n')
        user,time = csvline.split(",")
        usageObject['totalTime'] += int(time)
        if user in usageObject['userTime'].keys():
            usageObject['userTime'][user] += int(time)
        else:
            usageObject['userTime'][user] = int(time)
        csvfile.write(csvline+"\n")
        print("added {0} to total time, now laser life used is {1}".format(time,usageObject['totalTime']))
        usage = open('usage.json', 'w')
        usage.write(json.dumps(usageObject))
        usage.close()

