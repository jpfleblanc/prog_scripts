import math,zlib,numpy,sys
import os
import numpy
beta = float(sys.argv[1])
inputfile = sys.argv[2]


qx, qy, w, real_chi, im_chi= numpy.loadtxt(inputfile, unpack=True)

#print qx[0], qy[0], w[0], real_chi[0]

qlist=[]
for i in range(0, len(qx)):
#    print qxitem,qyitem
    if (qx[i],qy[i]) not in qlist:
      qlist.append((qx[i],qy[i]))


#print len(qlist)
freq_length=(len(set(w)))
wlist=sorted(set(w))
#print wlist

data_out=[]
chi_sum=numpy.zeros(freq_length)
print chi_sum

for s in range(0,len(qx)):

	data_array=[]

	for i in range(0,len(wlist)):
		#print w[s],wlist[i]
		if w[s]==wlist[i]:
			#print real_chi[s],chi_sum[i]
			#print chi_sum
			
			chi_sum[i]+=real_chi[s]/len(qlist)

print chi_sum

	
for i in range(0,len(wlist)):
	data_out.append((wlist[i],chi_sum[i]))



numpy.savetxt('DF_chi_local.dat',data_out)




