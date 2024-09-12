import math,zlib,numpy,sys
import os
import numpy



results=[]
FT=[]

for qx in numpy.linspace(0.000001,0.9999999, 600):
	for qy in numpy.linspace(0.000001,0.9999999, 600):
	
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
	

		beta=7.6
		dtau=beta/2.0
		#ft_result=(math.exp(-dtau*result)-1.0)/dtau
		#ft_result=result*(numpy.cosh(dtau*result)-numpy.cosh(0))/2.0/dtau
		#ft_result=result*(numpy.cosh(dtau*result))
		ft_result=result*(numpy.exp(-result*dtau)+numpy.exp( (beta-dtau)*(-result)))/(1.-numpy.exp(-result*beta))
		FT.append((qx,qy,ft_result))






numpy.savetxt('spinwave.dat', results)
numpy.savetxt('spinwaveFT.dat', FT)

