import math,zlib,numpy,sys
import os
import numpy
#beta = float(sys.argv[1])
inputfile = sys.argv[1]


qx, qy, w, real_chi, im_chi= numpy.loadtxt(inputfile, unpack=True)

slice_array=[]
qlist=[]

for i in range(0, len(qx)):

	if qx[i]>= numpy.pi/2 and qx[i] <= numpy.pi and qx[i]==qy[i]:
		if (qx[i],qy[i],w[i]) not in qlist:
			qlist.append((qx[i],qy[i],w[i]))
			slice_array.append((qx[i],qy[i],w[i],real_chi[i],im_chi[i]))
	if abs(qx[i]-numpy.pi)<0.0001 and qy[i] <= numpy.pi:
		if (qx[i],qy[i],w[i]) not in qlist:
			qlist.append((qx[i],qy[i],w[i]))
			slice_array.append((qx[i],qy[i],w[i],real_chi[i],im_chi[i]))
	if qx[i]>=numpy.pi and qx[i]<=numpy.pi*3/2 and abs(qy[i]-(qx[i]-numpy.pi))<0.0001:
		if (qx[i],qy[i],w[i]) not in qlist:
			qlist.append((qx[i],qy[i],w[i]))
			slice_array.append((qx[i],qy[i],w[i],real_chi[i],im_chi[i]))
	if qx[i]<=numpy.pi/2 and qy[i]==qx[i]:
		if (qx[i],qy[i],w[i]) not in qlist:
			qlist.append((qx[i],qy[i],w[i]))
			slice_array.append((qx[i],qy[i],w[i],real_chi[i],im_chi[i]))
	if qy[i]==0 and qx[i]<=numpy.pi:
		if (qx[i],qy[i],w[i]) not in qlist:
			qlist.append((qx[i],qy[i],w[i]))
			slice_array.append((qx[i],qy[i],w[i],real_chi[i],im_chi[i]))


numpy.savetxt('chi_slices.dat',slice_array)




