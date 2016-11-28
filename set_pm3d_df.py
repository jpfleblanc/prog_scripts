import math,zlib,numpy,sys
import os
import numpy
inputfile = sys.argv[1]
outputfile = sys.argv[2]

f = open(outputfile,'w')
#f.write('hi there\n') # python will convert \n to os.linesep
#f.close() 

qx, qy, w, real = numpy.loadtxt(inputfile, unpack=True)


qxlast=qx[0]
qylast=qy[0]
for i in range(0, len(qx)):
  if qx[i] != qxlast or qy[i] != qylast:
    qxlast=qx[i]
    qylast=qy[i]
    f.write("\n")
  f.write(str(qx[i])+" "+str(qy[i])+" "+str(w[i])+" "+str(real[i])+"\n")
  








