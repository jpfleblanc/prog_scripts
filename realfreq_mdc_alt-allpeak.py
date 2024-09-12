import math,zlib,numpy,sys
import os
import numpy
import operator
from peakutils.peak import indexes
#beta = float(sys.argv[1])
inputfile = sys.argv[1]


qx, qy, w, im_chi= numpy.loadtxt(inputfile, unpack=True)

wlist=[]

for i in range(0, len(w)):
#    print qxitem,qyitem
    if w[i] not in wlist and w[i]<1:
      wlist.append(w[i])


print "Freq list"
#print wlist


peak_array=[]


for s in range(0,len(wlist)):
	print str(s) +" out of " + str(len(wlist)) + " with value " +str(wlist[s])

	slice_array=[]
	chi_array=[]
	for i in range(0,len(w)):
		if w[i]==wlist[s] and wlist[s]<1 and wlist[s]>0:
			#print w[i], wlist[s]
			if abs(qx[i]-3.1415)<0.01 and qy[i]>3.13:
				slice_array.append((qy[i], w[i], im_chi[i]))
				chi_array.append(im_chi[i])

	print len(slice_array), len(chi_array)
	#print slice_array


	peak_indexes=[]
	peak_group_array=[]
	if len(slice_array)>0:
		
		#ind=numpy.argmax(slice_array)
		ind2=numpy.argmax(chi_array)
		print  ind2, slice_array[ind2][0],slice_array[ind2][1],slice_array[ind2][2]
		peak_array.append((slice_array[ind2][0]-3.14159265, slice_array[ind2][1]))


		if chi_array[0]>chi_array[1]:
				peak_indexes.append(0)
		for p in range(1,len(chi_array)-1):
			#print chi_array[p-1], chi_array[p] 
			if chi_array[p-1] < chi_array[p] and chi_array [p+1]< chi_array[p]:
				peak_indexes.append(p)

		for p in range(0,len(peak_indexes)):
			peak_group_array.append((slice_array[peak_indexes[p]][0]-3.14159265, slice_array[peak_indexes[p]][1]))
	
		print peak_indexes

	del slice_array[:]
	del chi_array[:]
	del peak_indexes[:]
	




numpy.savetxt('mdcpeaks-diag.dat',peak_array)
numpy.savetxt('mdcpeaks-all.dat',peak_group_array)




