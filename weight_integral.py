import math,zlib,numpy,sys
import os
import numpy
#beta = float(sys.argv[1])
inputfile = sys.argv[1]


qx, qy, w, chi= numpy.loadtxt(inputfile, unpack=True)

#print qx[0], qy[0], w[0], real_chi[0]

qlist=[]
for i in range(0, len(qx)):
#    print qxitem,qyitem
    if (qx[i],qy[i]) not in qlist:
      qlist.append((qx[i],qy[i]))


print len(qlist)

data_real=[]

for s in range(0,len(qlist)):
	print s

	data_array=[]

	for i in range(0, len(qx)):
		if qx[i]==qlist[s][0] and qy[i]==qlist[s][1] and w[i]>=0:
			if chi[i]>0:
				#data_array.append((w[i]*2.0*numpy.pi/beta, real_chi[i], 0.0001 ,im_chi[i], 0.0001))
				data_array.append((w[i], chi[i]))
				if w[i]==0:
					norm=real_chi[i]

	qsum=0.0
	for i in range(0,len(data_array)):
		if i>0:
			#print i, qsum, chi[i], (w[i]-w[i-1])
			qsum=qsum+data_array[i][1]*(data_array[i][0]-data_array[i-1][0])


	data_real.append((qlist[s][0],qlist[s][1], qsum))


	

numpy.savetxt('weight.dat',data_real)




