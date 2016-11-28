import math,zlib,numpy,sys
import os
import numpy
import cmath


# command line input
grealfile = sys.argv[1]
gimagfile = sys.argv[2]
fermi_cutoff=int(sys.argv[3])
boserange=int(sys.argv[4])
chi_file=sys.argv[5]


#loading G files
w,real_G = numpy.loadtxt(grealfile, usecols=(0,1), unpack=True)
w,imag_G = numpy.loadtxt(gimagfile, usecols=(0,1), unpack=True)
freq_num= len(w)

#One complex object
G=real_G+imag_G*1j

#deal with +/- frequency symmetry/antisymmetry
G_sym=numpy.zeros(2*len(w),dtype=complex)
for i in range(-len(w)+1,len(w)-1):
	if i <0:
		G_sym[i]=complex(-G[-i].real,G[-i].imag)
	else:
		G_sym[i]=complex(G[i].real,G[i].imag)

beta=2.0*numpy.pi/(w[1]-w[0])
bose_factor=beta*2.0*numpy.pi/beta
print "Beta is "+ str(beta)
print "cutoffs are " +str(fermi_cutoff)+" and "+str(boserange)


dataset=[]
sumdata=[]


chi=numpy.zeros(2*boserange+1, dtype=complex)

#bosonic range loop
for nb in range(-boserange,boserange):
	
#fermionic summation loop
	for wf in range(-boserange,boserange):
		
		W=wf+nb

		if abs(wf)>fermi_cutoff:
			chi[nb]+=-G_sym[wf]*G_sym[W]
		#print kx,ky,G_sqrd, chi
		

	print nb, chi[nb]
# need to check overall prefactors.
	dataset.append((nb, chi[nb].real/beta, chi[nb].imag/beta))

numpy.savetxt('dmft_gg_correction'+str(fermi_cutoff)+'_'+str(boserange)+'.dat',dataset)




qx, qy, w, real_chi, im_chi= numpy.loadtxt(inputfile, unpack=True)

chi_corrected_dataset=[]
for i in range(0,len(w)):
	bose=int(round(w[i]))
	chi_corrected_dataset.append((qx[i],qy[i],w[i], real_chi[i]+chi[bose].real/beta, im_chi[i]))

	

numpy.savetxt('chi_corrected.dat', chi_corrected_dataset)






