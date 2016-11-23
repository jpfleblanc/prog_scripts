import math,zlib,numpy,sys
import os
import numpy



results=[]

for qx in numpy.linspace(0,1, 600):
	for qy in numpy.linspace(0,1, 600):
	
		vqy=math.cos(2*numpy.pi*qy)
		vqx=math.cos(2*numpy.pi*qx)

		v2qy=math.cos(2*numpy.pi*2*qy)
		v2qx=math.cos(2*numpy.pi*2*qx)

		J=138.
		Jp=2.
		Jpp=2.
		Jc=38.
		t=330.
		zc=1.0#0.448
		J=J/t*zc
		Jp=Jp/t*zc
		Jpp=Jpp/t*zc
		Jc=Jc/t*zc

#		U=8.0
#		J=4./U- 24.0/U**3
#		Jc=80.0/U**3
#		Jp=Jc/20.0
#		Jpp=Jc/20.0



		A=J-Jc/2-(Jp-Jc/4)*(1-vqy*vqx)-Jpp*(1.0-(v2qx+v2qy)/2)
		B=(J-Jc/2)*(vqx+vqy)/2

		result=2.0*math.sqrt(A*A-B*B)
		results.append((qx,qy,result))


numpy.savetxt('spinwave.dat', results)

