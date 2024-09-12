#!/usr/bin/python

import sys
#uncomment to run on garching
#sys.path.append('/u/jleblanc/software/h5py-2.0.1/base/usr/local/lib64/python2.6/site-packages')
import sys, getopt;
import os, os.path, shutil, distutils.dir_util,numpy,h5py
from numpy import array,average
import re
import math
import resource


print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)


beta=str(sys.argv[1])
print "Beta is "+ beta

#os.system("python ~/working_2017/prog_scripts/extract_DF.py")
#os.system("python ~/working_2017/prog_scripts/extract_DF_chi.py")
os.system("python ~/working_2017/prog_scripts/realslice_reducer.py chi_extrapolated.dat")
os.system("python ~/working_2017/prog_scripts/ME_prep_james_lessfast.py "+beta+" chi_slices.dat")
os.system("python ~/working_2017/prog_scripts/peakfinder_slice.py realfreq.dat")
os.system("python ~/working_2017/prog_scripts/peakslice_plots.py peaks_slice.dat")


