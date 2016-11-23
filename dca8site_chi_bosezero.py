import math,zlib,numpy,sys
import os
import numpy
#beta = float(sys.argv[1])
inputfile = sys.argv[1]

clustername="Betts2D-8A"
qx, qy=numpy.loadtxt(open('/home/jpfleblanc/working_2016/cluster_momenta/momenta-'+clustername, 'r'), unpack=True)

chi = numpy.loadtxt(inputfile, unpack=True)

freq_num= 1#len(chi[:][1])
site_num=8

dataset=[]
sumdata=[]

chi_sum=numpy.zeros(freq_num)
#print chi_sum

for j in range(0,site_num):
	
	
	i=0
	chi_sum[i]+=chi[2*j]/site_num
	dataset.append((qx[j],qy[j], i-(freq_num-1)/2, chi[2*j]))




#print chi_sum
for i in range(0, len(chi_sum)):
	sumdata.append((i-(freq_num-1)/2, chi_sum[i]))

numpy.savetxt('dca_chi_manipulated.dat',dataset)
numpy.savetxt('dca_chi_local.dat',sumdata)




