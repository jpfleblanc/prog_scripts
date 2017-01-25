import math,zlib,numpy,sys
import os
import numpy
#beta = float(sys.argv[1])
inputfile = sys.argv[1]


qx, qy, w, chi= numpy.loadtxt(inputfile, unpack=True)

#print qx[0], qy[0], w[0], real_chi[0]

qlist=[]
qxlist=[]
qylist=[]
for i in range(0, len(qx)):
#    print qxitem,qyitem
    if (qx[i],qy[i]) not in qlist:
      qlist.append((qx[i],qy[i]))
    if qx[i] not in qxlist:
      qxlist.append(qx[i])
    if qy[i] not in qylist:
      qylist.append(qy[i])

print len(qxlist), len(qylist)

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
lambda_output=[]
single_val_w=[]
single_val_chi=[]


freq_length=len(w_slice)/len(qxlist)

for ival in range(0,len(qlist)):
	del single_val_w[:]
	del single_val_chi[:]
	for j in range(0, len(qx)):
		if abs(qx[j]-qlist[ival][0])<0.00001 and abs(qy[j]-qlist[ival][1]) <0.0001:
	#		print j, len(w)
			single_val_w.append(w[j])
			single_val_chi.append(chi[j])
#	print qxval
	print len(single_val_w)

#	if abs(qxval-3.14159265)<0.0001:
#		f = open('check.dat', "w")
#		for i in range(0,len(single_val_w)):
#			f.write(str(single_val_w[i])+" "+str(single_val_chi[i])+"\n")
	
	for j in range(0,len(single_val_w)):
		if j>0 and j< len(single_val_w)-1:
			if single_val_chi[j]>single_val_chi[j+1] and single_val_chi[j]>single_val_chi[j-1] and single_val_chi[j]>1e-4 and single_val_w[j]<1.5:
				final_output.append((qlist[ival][0], qlist[ival][1], single_val_w[j], single_val_chi[j]))
				jmax=j
				maxval=single_val_chi[j]
				maxw=single_val_w[j]
				break

	print maxval, maxw
	for j in range(1,jmax):
		if single_val_chi[j]>maxval/2.0 and single_val_chi[j-1]<maxval/2.0:
			half_point=single_val_w[j]
			lambda_output.append((qlist[ival][0], qlist[ival][1], maxw-half_point))
			break
			



#for i in range(0,len(qx_slice)):
#	if 
	#print qx_slice



	
#data_real=[]


numpy.savetxt('peaks_slice.dat',final_output)
numpy.savetxt('lambda_slice.dat',lambda_output)




