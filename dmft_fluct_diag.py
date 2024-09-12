import math,zlib,numpy,sys
import os
import numpy
import cmath

print(sys.argv)
# command line input
gfile = sys.argv[1]
vertex_file=sys.argv[2]
Uvalue=float(sys.argv[3])
#fermi_cutoff=int(sys.argv[3])
#boserange=int(sys.argv[4])


#loading G file
w,real_G, imag_G = numpy.loadtxt(gfile, comments='#', usecols=(0,1,2), unpack=True)
#w,imag_G = numpy.loadtxt(gimagfile, usecols=(0,1), unpack=True)
freq_num= len(w)




#One complex object
G=real_G+imag_G*1j

#deal with +/- frequency symmetry/antisymmetry
G_sym=numpy.zeros(2*len(w),dtype=complex)
for i in range(-len(w),len(w)):
	if i <0:
		G_sym[i]=complex(-G[-i-1].real,G[-i-1].imag)
	else:
		G_sym[i]=complex(G[i].real,G[i].imag)


#print(G_sym[0],G_sym[-1],G_sym[1], G_sym[-2])

beta=2.0*numpy.pi/(w[1]-w[0])
bose_factor=beta*2.0*numpy.pi/beta
print "Beta is "+ str(beta)
print("U is " +str(Uvalue))
#print "cutoffs are " +str(fermi_cutoff)+" and "+str(boserange)

#load vertex
print("Reading full vertex file")
omega, nu, nup, Re_F_ud, Im_F_ud, Re_F_uu, Im_F_uu= numpy.loadtxt(vertex_file, comments='#', usecols=(0,1,2,3,4,5,6), unpack=True)
print("Reading vertex file complete")

# create lists of omega, nu, nup

print("Creating lists")
omegalist=[]
nulist=[]
nuplist=[]
for i in range(0, len(omega)):
	if omega[i] not in omegalist:
		omegalist.append(omega[i])
	if nu[i] not in nulist:
		nulist.append(nu[i])
	if nup[i] not in nuplist:
		nuplist.append(nup[i])


print("Constructing Fsp - start")

#F_ud=numpy.zeros((len(omegalist),len(nulist),len(nuplist)),dtype=complex)
#F_uu=numpy.zeros((len(omegalist),len(nulist),len(nuplist)),dtype=complex)
F_sp=numpy.zeros((len(omegalist),len(nulist),len(nuplist)),dtype=complex)

for i in range (0,len(Re_F_ud)):
	#F_sp[omega[i]][nu[i]][nup[i]]=complex(Re_F_uu[i],Im_F_uu[i])-complex(Re_F_ud[i],Im_F_ud[i])
	F_sp[omega[i]][nu[i]][nup[i]]=complex(Re_F_ud[i],Im_F_ud[i])
	#F_uu[omega[i]][nu[i]][nup[i]]=complex(Re_F_uu[i],Im_F_uu[i])	

#print(F_ud[-24][22][5], F_uu[-24][22][5])
print("Constructing Fsp - complete")


print("Beginning summation")
sigma_fluct_dmft=numpy.zeros((len(nulist),len(omegalist)),dtype=complex)
sigma_sum_dmft=numpy.zeros((len(nulist)),dtype=complex)

for w in range(0, len(omegalist)):
	for n in range(0, len(nulist)):
		for np in range (0, len(nuplist)):
			sigma_fluct_dmft[nulist[n]][omegalist[w]]=sigma_fluct_dmft[nulist[n]][omegalist[w]]+ F_sp[omegalist[w]][nulist[n]][nuplist[np]]*G_sym[nuplist[np]]*G_sym[nuplist[np]+omegalist[w]]*G_sym[nulist[n]+omegalist[w]]*Uvalue/beta/beta
			
for w in range(0, len(omegalist)):
	for n in range(0, len(nulist)):
		sigma_sum_dmft[nulist[n]]=sigma_sum_dmft[nulist[n]]+sigma_fluct_dmft[nulist[n]][omegalist[w]]


print("Summation complete - Sorting for file writing")
results_fluct=[]
results_sum=[]
for n in range(0, len(nulist)):
	results_sum.append((nulist[n],sigma_sum_dmft[nulist[n]].real,sigma_sum_dmft[nulist[n]].imag))
	for w in range(0, len(omegalist)):
		results_fluct.append((nulist[n],omegalist[w], sigma_fluct_dmft[nulist[n]][omegalist[w]].real, sigma_fluct_dmft[nulist[n]][omegalist[w]].imag))
		


numpy.savetxt("sigma_fluct_dmft.dat", results_fluct)
numpy.savetxt("sigma_sum.dat", results_sum)





