#!/usr/bin/python

import Adafruit_BBIO.ADC as ADC
import time
import datetime
import numpy as np

ADC.setup()

# Based on observation of high and low raw readings X 3.6 V. Then took the average of each.
zeroOffsetX = 1.595
zeroOffsetY = 1.614
zeroOffsetZ = 1.672

#The sensitivity or conversion factor is the average for each axis minus low raw reading.
conversionFactorX = 0.319
conversionFactorY = 0.325
conversionFactorZ = 0.322

# Make sure the out file is opened properly
while 1:
  try:
    f1 = open('/media/CARD/acceleration2.csv','a')
    f2 = open('/media/CARD/acceleration_errors2.csv','a')
    print "Successfully opened", f1.name
    print "Successfully opened", f2.name
    f1.write("Month,Day,Hour,Minute,Second,Xraw,Yraw,Zraw,X,Y,Z,Norm\n")
    f2.write("Month,Day,Hour,Minute,Second,Error\n")
    break
  except Exception as error1:
    print 'Error ' + str(error1)
    time.sleep(1)

# Get accelerometer values and write them to file
while 1:
  try:
    now = datetime.datetime.now()
    rawX =  ADC.read("P9_36")
    rawY =  ADC.read("P9_38")
    rawZ =  ADC.read("P9_40")

    # Convert raw values to g values 
    # Reference: http://beagleboard.org/support/BoneScript/accelerometer/
    Xvalue = ((rawX * 3.6) - zeroOffsetX)/conversionFactorX
    Yvalue = ((rawY * 3.6) - zeroOffsetY)/conversionFactorY
    Zvalue = ((rawZ * 3.6) - zeroOffsetZ)/conversionFactorZ
    
    # raw input is multiplied by 3.6 because it has to be multiplied by 1.8 to get voltage and since it is hooked up to a voltage
    # divider it also needs to be multiplied by 2 to get the original voltage
    print 'X: ' + str(Xvalue)
    print 'Y: ' + str(Yvalue)
    print 'Z: ' + str(Zvalue)
    a = np.array([Xvalue, Yvalue, Zvalue])
    print 'Norm: ' + str(np.linalg.norm(a))
    print 'Xraw: ' + str(rawX * 3.6)
    print 'Yraw: ' + str(rawY * 3.6) 
    print 'Zraw: ' + str(rawZ * 3.6)
    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(rawX)+','+str(rawY)+','+str(rawZ)+','+str(Xvalue)+','+str(Yvalue)+','+str(Zvalue)+','+str(np.linalg.norm(a))+'\n')
  except Exception as error2:
    print 'Error ' + str(error2)
    f2.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(error2)+'\n');
  time.sleep(1)

f1.close()
f2.close()
