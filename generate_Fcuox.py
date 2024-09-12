import math,zlib,numpy,sys
import os
import numpy


def chi(omega, epsilon):
	return 1.0/(1.0j*omega+epsilon+.01j)
def ft_chi(tau, epsilon):
	sum_ft=0+0j
	for omega in numpy.arange(-150,150):
		omega_n=2*numpy.pi/beta*omega
		sum_ft+=chi(omega,epsilon)*numpy.exp(-1j*omega_n*tau)

	return sum_ft

def Fcu(qx,qy):
	return (0.84+2.0*(numpy.cos(qx)+numpy.cos(qy)))**2

def Fox(qx,qy):
	return 2.0*0.91*(1.0+0.5*(numpy.cos(qx)+numpy.cos(qy)))





Fcopper=[]
Foxygen=[]

max_index=2048
for qx_index in numpy.arange(0,max_index):
	for qy_index in numpy.arange(0,max_index):
		qx=qx_index*2.0*numpy.pi/max_index
		qy=qy_index*2.0*numpy.pi/max_index
		Fcopper.append((qx,qy,Fcu(qx,qy)))
		Foxygen.append((qx,qy,Fox(qx,qy)))




numpy.savetxt('Fcu.dat', Fcopper)
numpy.savetxt('Fox.dat', Foxygen)

