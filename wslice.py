import math,zlib,numpy,sys
import os
import numpy
#beta = float(sys.argv[1])
inputfile = sys.argv[1]


os.system("awk '$1==3.141592653589793116 && $2==$1 && $3 > 0 {print}' "+inputfile+" > wslice_pipi.dat")
os.system("awk '$1==3.141592653589793116 && $2==0 && $3 > 0{print}' "+inputfile+" > wslice_piz.dat")
os.system("awk '$1==1.570796326794896558 && $2==1.570796326794896558 && $3 > 0{print}' "+inputfile+" > wslice_pi2pi2.dat")

