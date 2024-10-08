import math,zlib,numpy,sys
import os
import numpy
beta = float(sys.argv[1])
inputfile = sys.argv[2]


qx, qy, w, real_g, im_g= numpy.loadtxt(inputfile, unpack=True)

#print qx[0], qy[0], w[0], real_chi[0]

qlist=[]
for i in range(0, len(qx)):
#    print qxitem,qyitem
    if (qx[i],qy[i]) not in qlist:
      qlist.append((qx[i],qy[i]))


print len(qlist)

data_real=[]

for s in range(0,len(qlist)):

	data_array=[]

	for i in range(0, len(qx)):
		if qx[i]==qlist[s][0] and qy[i]==qlist[s][1] and w[i]>=0:
			#if real_q[i]>0:
			#data_array.append((w[i]*2.0*numpy.pi/beta, real_chi[i], 0.0001 ,im_chi[i], 0.0001))
			data_array.append(((w[i]+0.5)*2.0*numpy.pi/beta, real_g[i], 0.004 ,im_g[i], 0.004))#0.00004 ,im_g[i], 0.00004))
			if w[i]==0:
				norm=1
					#norm=real_chi[i]

	#print data_array
		
	numpy.savetxt("dat_in", data_array)
	ndat=len(data_array)

	del data_array[:]

	parm_file=open("maxent.parm",'w')
	parm_file.write("N_ALPHA = 20\nALPHA_MIN = 0.1\nALPHA_MAX = 100\n")
	parm_file.write("NORM = 1\n")#+str(norm)+"\n")
	parm_file.write("OMEGA_MAX = 12\n")
	parm_file.write("KERNEL = fermionic\n")
	parm_file.write("BETA = "+str(beta)+"\n")
	parm_file.write("NFREQ = 800\n")
	parm_file.write("NDAT = "+str(2*ndat)+"\n")
	parm_file.write("FREQUENCY_GRID = quadratic\n")#Lorentzian\n") linear\n")#
	parm_file.write("DATASPACE =frequency\n")
	parm_file.write("MAX_IT = 400\n")
	parm_file.write("DEFAULT_MODEL =\"gaussian\"\n")#flat\"\n")#gaussian\"\n")
	#parm_file.write("DEFAULT_MODEL = \"linear rise exp decay\" \n")#\"quadratic rise exp decay\"\n")
	parm_file.write("LAMBDA = 1.0 \n")
	parm_file.write("TEXT_OUTPUT = 1\n")
	parm_file.write("SELF = 0\n")
	parm_file.write("SIGMA = 1.5\n")
	parm_file.write("PARTICLE_HOLE_SYMMETRY = 0\n")
#	parm_file.write("GENERATE_ERR = 0\n")
	parm_file.write("DATA = dat_in\n")


	parm_file.close()

	os.system("$HOME/alps_core/Maxent/install/maxent maxent.parm")

	w_real, chi_real, chi_im = numpy.loadtxt('maxent.out.avspec.dat', usecols=(0,1,2), unpack=True)

	for m in range(0,len(w_real)):
		data_real.append((qlist[s][0],qlist[s][1], w_real[m], chi_real[m], chi_im[m]))

numpy.savetxt('realfreq_fermionic.dat',data_real)




