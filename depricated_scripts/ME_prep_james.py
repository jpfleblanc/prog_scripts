import math,zlib,numpy,sys
import os
import numpy
beta = float(sys.argv[1])
inputfile = sys.argv[2]
parm_file=open("maxent.parm",'w')

qx, qy, w, real_chi, im_chi= numpy.loadtxt(inputfile, unpack=True)

#print qx[0], qy[0], w[0], real_chi[0]

data_array=[]

for i in range(0, len(qx)):
	if qx[i]==1.5708 and qy[i]==1.5708 and w[i]>=0:
		data_array.append((w[i]*2.0*numpy.pi/beta, real_chi[i], real_chi[i]*0.02,im_chi[i], im_chi[i]*0.02))
		if w[i]==0:
			norm=real_chi[i]

#print data_array
		
numpy.savetxt("dat_in", data_array)


parm_file.write("N_ALPHA = 80\nALPHA_MIN = 0.05\nALPHA_MAX = 15\n")
parm_file.write("NORM = "+str(norm)+"\n")
parm_file.write("OMEGA_MAX = 40\n")
parm_file.write("KERNEL = bosonic\n")
parm_file.write("BETA = "+str(beta)+"\n")
parm_file.write("NFREQ = 500\n")
parm_file.write("NDAT = 10\n")
parm_file.write("FREQUENCY_GRID = Lorentzian\n")
parm_file.write("DATASPACE =frequency\n")
parm_file.write("MAX_IT = 16000\n")
parm_file.write("DEFAULT_MODEL =\"gaussian\"\n")
parm_file.write("TEXT_OUTPUT = 1\n")
parm_file.write("SELF = 0\n")
parm_file.write("SIGMA = 3\n")
parm_file.write("PARTICLE_HOLE_SYMMETRY = 0\n")
parm_file.write("DATA = dat_in\n")


parm_file.close()

