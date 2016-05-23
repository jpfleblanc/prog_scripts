import math,zlib,numpy,sys
import os
import numpy

beta = float(sys.argv[1])
inputfile = sys.argv[2]


qx, qy, w, real_chi, im_chi= numpy.loadtxt(inputfile, unpack=True)

#print qx[0], qy[0], w[0], real_chi[0]

print 1+1.j

qlist=[]
for i in range(0, len(qx)):
#    print qxitem,qyitem
    if (qx[i],qy[i]) not in qlist:
      qlist.append((qx[i],qy[i]))


print len(qlist)

data_FT=[]
dtau=0.001

for s in range(0,len(qlist)):

	data_array=[]

	for i in range(0, len(qx)):
		if qx[i]==qlist[s][0] and qy[i]==qlist[s][1] and w[i]>=0:
			if real_chi[i]>0:
				#data_array.append((w[i]*2.0*numpy.pi/beta, real_chi[i], 0.0001 ,im_chi[i], 0.0001))
				data_array.append((w[i]*2.0*numpy.pi/beta, real_chi[i], 0.000051 ,im_chi[i], 0.0001))
				if w[i]==0:
					norm=real_chi[i]

	#print data_array

	sum_dtau=0#+0j
	sum_zero=0#+0j
	for j in range(0,len(data_array)):
		sum_dtau+=data_array[j][1]*numpy.exp(-1.j*data_array[j][0]*dtau)
		sum_zero+=data_array[j][1]

	ft_result=(sum_dtau-sum_zero)/dtau

	#data_FT.append((qlist[s][0],qlist[s][1], numpy.real(ft_result), numpy.imag(ft_result)))
	data_FT.append((qlist[s][0],qlist[s][1], ft_result))






		
	#numpy.savetxt("dat_in", data_array)
	ndat=len(data_array)

	del data_array[:]



numpy.savetxt('FT.dat',data_FT)




