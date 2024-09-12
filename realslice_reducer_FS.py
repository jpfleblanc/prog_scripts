import math,zlib,numpy,sys
import os
import numpy
#beta = float(sys.argv[1])
inputfile = sys.argv[1]


qx, qy, w, real_chi, im_chi= numpy.loadtxt(inputfile, unpack=True)

slice_array=[]
qlist=[]

for i in range(0, len(qx)):


	if abs(qy[i]+(qx[i]-numpy.pi))<0.0001:
		if (qx[i],qy[i],w[i]) not in qlist:
			qlist.append((qx[i],qy[i],w[i]))
			slice_array.append((qx[i],qy[i],w[i],real_chi[i],im_chi[i]))
	


numpy.savetxt('gkxky_FS.dat',slice_array)




