import math,zlib,numpy,sys
import os
import numpy
beta = float(sys.argv[1])
inputfile = sys.argv[2]


qx, qy, w, real_chi, im_chi= numpy.loadtxt(inputfile, unpack=True)

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
	data_shifted=[]
	for i in range(0, len(qx)):
		if qx[i]==qlist[s][0] and qy[i]==qlist[s][1] and w[i]>=0:
			if real_chi[i]>0:
				#data_array.append((w[i]*2.0*numpy.pi/beta, real_chi[i], 0.0001 ,im_chi[i], 0.0001))
				#set im_chi[i] to zero



				data_array.append((w[i]*2.0*numpy.pi/beta, real_chi[i], 0.00015 + real_chi[i]*0.002  ,im_chi[i], 0.00015))

				if w[i]==0:
					norm=real_chi[i]
	
	for i in range(0,len(data_array)):
		#print i,len(data_array)-1, data_array[len(data_array)-1][1], data_array[i][4]
		data_shifted.append((data_array[i][0],data_array[i][1]-data_array[len(data_array)-1][1], data_array[i][2], data_array[i][3], data_array[i][4]))

	#print data_array
		
	numpy.savetxt("dat_in", data_shifted)
#	numpy.savetxt("dat_in", data_array)
	ndat=len(data_array)

	del data_array[:]

	parm_file=open("maxent.parm",'w')

	parm_file.write("N_ALPHA = 30\nALPHA_MIN = 0.015\nALPHA_MAX = 150\n")
	parm_file.write("NORM = "+str(norm)+"\n")
	parm_file.write("OMEGA_MAX = 8\n")
	parm_file.write("KERNEL = bosonic\n")
	parm_file.write("BETA = "+str(beta)+"\n")
	parm_file.write("NFREQ = 1200\n")
	parm_file.write("NDAT = "+str(2*ndat)+"\n")
	parm_file.write("FREQUENCY_GRID = log\n")#quadratic\n")#log\n")#quadratic\n")#Lorentzian\n")
	parm_file.write("DATASPACE =frequency\n")
	parm_file.write("MAX_IT = 1200\n")
	parm_file.write("DEFAULT_MODEL =\"gaussian\"\n")
	#parm_file.write("DEFAULT_MODEL = \"linear rise exp decay\" \n")#\"quadratic rise exp decay\"\n")
	parm_file.write("LAMBDA = 1.0 \n")
	parm_file.write("TEXT_OUTPUT = 1\n")
	parm_file.write("SELF = 0\n")
	parm_file.write("SIGMA = 1.0\n")
	parm_file.write("PARTICLE_HOLE_SYMMETRY = 0\n") # check kernel type
	parm_file.write("GENERATE_ERR = 0\n")
	parm_file.write("DATA = dat_in\n")


	parm_file.close()

	os.system("$HOME/alps_core/Maxent/install/maxent maxent.parm")

	w_real, chi_real = numpy.loadtxt('maxent.out.avspec_bose.dat', usecols=(0,1), unpack=True)

	for m in range(0,len(w_real)):
		data_real.append((qlist[s][0],qlist[s][1], w_real[m], chi_real[m]))

numpy.savetxt('realfreq.dat',data_real)




