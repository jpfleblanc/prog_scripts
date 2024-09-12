import math,zlib,numpy,sys
import os
import numpy
#beta = float(sys.argv[1])
inputfile = sys.argv[1]


qx, qy, w, chi= numpy.loadtxt(inputfile, unpack=True)

#print qx[0], qy[0], w[0], real_chi[0]

wlist=[]

for i in range(0, len(w)):
#    print qxitem,qyitem
    if w[i] not in wlist:
      wlist.append(w[i])
   
print 'Wlist has '+str(len(wlist))+" items"

final_output=[]
for ival in range(0,len(wlist)):
	print ival
	qsum=0.0
	count=0.0
	for j in range(0, len(w)):
		if abs(w[j]-wlist[ival])<0.00001:
	#		print j, len(w)
			qsum+=chi[j]
			count=count+1.0
			
	final_output.append((wlist[ival], qsum/float(count)))



numpy.savetxt('qaverage.dat',final_output)




