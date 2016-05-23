import math,zlib,numpy,sys
import os
import numpy
#beta = float(sys.argv[1])
inputfile = sys.argv[1]


qx, qy, wp, chip= numpy.loadtxt(inputfile, unpack=True)


slice1=[]
slice2=[]
slice3=[]
slice4=[]
slice5=[]

for i in range(0, len(qx)):

	if qx[i]>= numpy.pi/2 and qx[i] <= numpy.pi and qx[i]==qy[i]:
		length=(qx[i]-numpy.pi/2)*math.sqrt(2)
		slice1.append((qx[i],qy[i],wp[i],chip[i],length))
	if abs(qx[i]-numpy.pi)<0.0001 and qy[i] <= numpy.pi:
		length=(numpy.pi-qy[i]) + numpy.pi/math.sqrt(2)
		slice2.append((qx[i],qy[i],wp[i],chip[i],length))
	if qx[i]>=numpy.pi and qx[i]<=numpy.pi*3/2 and abs(qy[i]-(qx[i]-numpy.pi))<0.0001:
		length=qy[i]*math.sqrt(2) + numpy.pi + numpy.pi/math.sqrt(2)
		slice3.append((qx[i],qy[i],wp[i],chip[i],length))
	if qx[i]<=numpy.pi/2 and qy[i]==qx[i]:
		length=numpy.pi/2-qx[i] + numpy.pi + numpy.pi*math.sqrt(2)
		slice4.append((qx[i],qy[i],wp[i],chip[i],length))
	if qy[i]==0 and qx[i]<=numpy.pi:
		length=qx[i] + numpy.pi + 2*numpy.pi/math.sqrt(2) + numpy.pi/2.0
		slice5.append((qx[i],qy[i],wp[i],chip[i],length))


numpy.savetxt('slice1.dat',slice1)
numpy.savetxt('slice2.dat',slice2)
numpy.savetxt('slice3.dat',slice3)
numpy.savetxt('slice4.dat',slice4)
numpy.savetxt('slice5.dat',slice5)




