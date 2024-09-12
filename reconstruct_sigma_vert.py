
import h5py
import numpy 
from numpy import pi
import re
import sys
import cmath
#import complex

vert_file=sys.argv[1]
g_file=sys.argv[2]

print("Loading G")
w, re_g,im_g =numpy.loadtxt(g_file, usecols=(0,1,2), unpack=True)

#print w, len(re_g)

G_full=numpy.zeros(2*len(re_g), dtype=complex)
F_full=numpy.zeros( (65, 128,128), dtype=complex)
#print G_full

for i in range (0,2048):
	if i < len(re_g):
		G_full[i]=re_g[i]+im_g[i]*1j
	else:
		G_full[i]=re_g[-i+len(re_g)-1]-im_g[-i+len(re_g)-1]*1j

	#print(i,G_full[i])


print("G Loaded and parsed")

print("Loading F")

w=[]
nu=[]
nup=[]
reFuu=[]
imFuu=[]
reFud=[]
imFud=[]
w, nu, nup, reFuu,imFuu, reFud, imFud=numpy.loadtxt(vert_file, unpack=True)

for i in range(0,len(reFud)):
	#F_full[w[i]][nu[i]][nup[i]]= reFud[i]+imFud[i]*1j    #reFuu[i]+imFuu[i]*1j        #reFud[i]+imFud[i]*1j
	F_full[w[i]][nu[i]][nup[i]]= reFud[i]+imFud[i]*1j -reFuu[i] - imFuu[i]*1j

#print F_full[0][2][1]
print("F Loaded")


U=8
beta=5



sigma=[]

for nu in range(-64,64):
	total=0
	print nu
	for w in range(-32,33):
		for nup in range(-64,64):
			total=total+F_full[w][nu][nup]*G_full[nup]*G_full[nup+w]*G_full[nu+w]/numpy.pi


	sigma.append((nu, numpy.pi/beta*(2*nu+1), -U/beta/beta*total.real, -U/beta/beta*total.imag ))


numpy.savetxt("output.dat", sigma)

g_result=[]
for i in range(0, len(G_full)):
	g_result.append((i, G_full[i].real, G_full[i].imag))

numpy.savetxt("parsed_G.dat",g_result)


















