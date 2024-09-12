


import sys

import sys, getopt;
import os, os.path, shutil, distutils.dir_util,numpy,h5py
from numpy import array,average
import re
import math
import resource

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def func(x, a, b,c ):
	

	return a/((x-numpy.pi)**2+(b)**2) +c



start_directory=os.getcwd()


#big_f=int(sys.argv[1])

#os.system("awk '$1==3.141592653589793116e+00 && $3==0{print}' chi_extrapolated.dat > chi_pislice.dat ")


print "Reading first chi"
qx, qy, w, real_chi, im_chi= numpy.loadtxt("data.dat", unpack=True)



popt, pcov = curve_fit(func, qy, real_chi, bounds=(0, [100., 100.,100.]))

print popt, pcov

xi=1.0/popt[1]

print "xi is "
print xi, popt[0],popt[1], popt[2]

os.system("echo "+str(xi)+" > xi.dat")

output=[]
for x in numpy.arange(0,2*numpy.pi, numpy.pi/60):
	output.append((x,func(x,popt[0],popt[1],popt[2])))

#print(output)

numpy.savetxt("fit.dat", output)



#xi_in=numpy.loadtxt("xi.dat")

#print xi_in





