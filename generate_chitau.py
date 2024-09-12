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


results=[]
FT=[]

epsilon=1.0
beta=5.0
for omega in numpy.arange(-20,20):
	omega_n=2*numpy.pi/beta*omega
	value=chi(omega_n,epsilon)
	results.append((omega_n, numpy.real(value),numpy.imag(value)))



dtau=0.001
for dtau in numpy.linspace(-10,10,500):
	FT_result=ft_chi(dtau,epsilon)
	FT.append((dtau, numpy.real(FT_result), numpy.imag(FT_result)))




numpy.savetxt('chi_omega.dat', results)
numpy.savetxt('chi_tau.dat', FT)

