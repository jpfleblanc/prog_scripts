


import sys

import sys, getopt;
import os, os.path, shutil, distutils.dir_util,numpy,h5py
from numpy import array,average
import re
import math
import resource

start_directory=os.getcwd()


big_f=int(sys.argv[1])
inputdir_big = sys.argv[2]
small_f=int(sys.argv[3])
inputdir_small = sys.argv[4]

os.chdir(inputdir_big)
#os.system("python ~/working/prog_scripts/run_bubble_correction.py "+str(big_f) )
os.chdir(inputdir_small)
#os.system("python ~/working/prog_scripts/run_bubble_correction.py "+str(small_f) )


print "Reading first chi"
qx, qy, w, real_chi_big, im_chi_big= numpy.loadtxt(inputdir_big+"/chi_corrected.dat", unpack=True)
print "Reading second chi"
qx2, qy2, w2, real_chi_small, im_chi_small= numpy.loadtxt(inputdir_small+"/chi_corrected.dat", unpack=True)

### exit catch for something wrong
if len(qx) != len(qx2):
	print "Lengths don't match!!! Exiting"
	exit()
###

#data1-(data2-data1)*(1./nomega1)/(1./nomega2-1./nomega1)

os.chdir(start_directory)
chi_extrap=[]

for i in range(0,len(real_chi_big)):


  if real_chi_big[i] > real_chi_small[i]:
    real_part= real_chi_big[i] - (real_chi_small[i]-real_chi_big[i])*(1.0/float(big_f))/(1.0/float(small_f) - 1.0/float(big_f)  )
  else:
    real_part=real_chi_big[i]
  imag_part= im_chi_big[i] - (im_chi_small[i]-im_chi_big[i])*(1.0/float(big_f))/(1.0/float(small_f) - 1.0/float(big_f)  )
  chi_extrap.append((qx[i], qy[i],w[i], real_part, imag_part))

numpy.savetxt('chi_extrapolated.dat', chi_extrap)


