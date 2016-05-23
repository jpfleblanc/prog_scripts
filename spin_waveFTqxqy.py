import math,zlib,numpy,sys
import os
import numpy

def spec(epsilon, omega, gamma):
	return gamma/2.0/((epsilon-omega)**2+gamma**2)

results=[]
FT=[]

qx=numpy.pi
qy=numpy.pi

vqy=math.cos(2*numpy.pi*qy)
vqx=math.cos(2*numpy.pi*qx)

v2qy=math.cos(2*numpy.pi*2*qy)
v2qx=math.cos(2*numpy.pi*2*qx)

J=138.
Jp=2.
Jpp=2.
Jc=38.
t=330.
J=J/t
Jp=Jp/t
Jpp=Jpp/t
Jc=Jc/t

A=J-Jc/2-(Jp-Jc/4)*(1-vqy*vqx)-Jpp*(1.0-(v2qx+v2qy)/2)
B=(J-Jc/2)*(vqx+vqy)/2

result=math.sqrt(A*A-B*B)
results.append((qx,qy,result))

dtau=0.001
beta=5.0
gamma=0.05

sum_chi=0
epsilon=result

chi_omega=[]

delta=20./10000.

for omega in numpy.arange(-50,50):
	print omega
	omega_n=2*numpy.pi/beta*omega
	sum_chi=0+0j
	for omega_real in numpy.linspace(-10,10,10000):
		sum_chi+=spec(omega_real,epsilon,gamma)/(omega_n+omega_real)*delta

	chi_omega.append((omega_n, numpy.real(sum_chi), numpy.imag(sum_chi)))


for tau in numpy.linspace(-10,10,1000):
#ft_result=(math.exp(-dtau*result)-1.0)/dtau
#ft_result=result*(numpy.cosh(dtau*result)-numpy.cosh(0))/2.0/dtau
	ft_result=0+0j
	for i in range(0, len(chi_omega)):
		chi=chi_omega[i][1]+1.j*chi_omega[i][2]
		ft_result+=chi*numpy.exp(-1j*chi_omega[i][0]*tau)
	FT.append((tau,numpy.real(ft_result), numpy.imag(ft_result)))






numpy.savetxt('spinwave_chiomega.dat', chi_omega)
numpy.savetxt('spinwave_chitau.dat', FT)

