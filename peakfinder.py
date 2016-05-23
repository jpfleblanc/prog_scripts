import math,zlib,numpy,sys
import os
import numpy
#beta = float(sys.argv[1])
inputfile = sys.argv[1]


qx, qy, w, chi= numpy.loadtxt(inputfile, unpack=True)

#print qx[0], qy[0], w[0], real_chi[0]

qlist=[]
qxlist=[]
for i in range(0, len(qx)):
#    print qxitem,qyitem
    if (qx[i],qy[i]) not in qlist:
      qlist.append((qx[i],qy[i]))
    if qx[i] not in qxlist:
      qxlist.append(qx[i])

print qxlist

qx_slice=[]
w_slice=[]
chi_slice=[]
for i in range(0,len(qx)):
	if abs(qy[i]-3.14159265)<0.001:
#		print qy[i]
		#slice.append((qx[i],w[i],chi[i]))
		qx_slice.append(qx[i])
		w_slice.append(w[i])
		chi_slice.append(chi[i])


	final_output=[]
	single_val_w=[]
	single_val_chi=[]
for qxval in qxlist:
	del single_val_w[:]
	del single_val_chi[:]
	for j in range(0, len(qx_slice)):
		if abs(qx_slice[j]-qxval)<0.00001:
			single_val_w.append(w_slice[j])
			single_val_chi.append(chi_slice[j])
	print qxval
	print len(single_val_w)

	if abs(qxval-3.14159265)<0.0001:
		f = open('check.dat', "w")
		for i in range(0,len(single_val_w)):
			f.write(str(single_val_w[i])+" "+str(single_val_chi[i])+"\n")
	
	for j in range(0,len(single_val_w)):
		if j>0 and j< len(single_val_w)-1:
			if single_val_chi[j]>single_val_chi[j+1] and single_val_chi[j]>single_val_chi[j-1] and single_val_chi[j]>1e-4 and single_val_w[j]<1.5:
				final_output.append((qxval, single_val_w[j]))#, single_val_chi[i]))




#for i in range(0,len(qx_slice)):
#	if 
	#print qx_slice



	
#data_real=[]


numpy.savetxt('peaks.dat',final_output)




