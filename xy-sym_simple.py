import math,zlib,numpy,sys
import os
import numpy
#beta = float(sys.argv[1])
inputfile = sys.argv[1]
outfile=sys.argv[2]


qx, qy, w, real_chi= numpy.loadtxt(inputfile, unpack=True)


qlist=[]
wlist=[]

for i in range (0, len(w)):
  if qx[i] not in qlist:
    qlist.append(qx[i])

  if w[i] not in wlist:
    wlist.append(w[i])

print len(qlist),len(wlist)


output=[]

for i in range(0, len(wlist)):
  print i

  for full_i in range(len(wlist)*i,len(wlist)*(i+1)):
    for full_j in range(len(wlist)*i,len(wlist)*(i+1)):
      if w[full_i]==w[full_j]:
	if qx[full_j]==qy[full_i] and qy[full_j]==qx[full_i]:
	  jindex=full_j
	  break 


    output.append((qx[full_i],qy[full_i],w[full_i], (real_chi[full_i]+real_chi[jindex])/2.0))

numpy.savetxt(outfile,output)



#numpy.savetxt('chi-mod.dat',slice_array)




