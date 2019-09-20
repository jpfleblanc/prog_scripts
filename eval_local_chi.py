import os, numpy


def F_Cu_squared(qx,qy):
	output=(0.84+2.0*(numpy.cos(qx)+numpy.cos(qy)) )**4
	return output

def F_O_squared(qx,qy):
	output=(2*.91**2*(1.0+(numpy.cos(qx)+numpy.cos(qy) )  )  )**2
	return output

qx,qy,w,chi=numpy.loadtxt('../realfreq_pos.dat', unpack=True)

print qx

w_list=[]
q_list=[]

for i in range(0,len(chi)):
	if w[i] not in w_list:
		w_list.append(w[i])

	if qx[i] not in q_list:
		q_list.append(qx[i])

print len(w_list), len(q_list)

result=numpy.zeros(len(w_list))
result_Cu=numpy.zeros(len(w_list))
result_O=numpy.zeros(len(w_list))

for i in range(0,len(chi)):
	#print i
	for j in range(0,len(w_list)):
		if w[i]==w_list[j]:
			result[j]=result[j]+chi[i]
			result_Cu[j]=result_Cu[j]+chi[i]*F_Cu_squared(qx[i],qy[i])
			result_O[j]=result_O[j]+chi[i]*F_O_squared(qx[i],qy[i])

result=result/len(q_list)**2

output=[]

for i in range(0,len(w_list)):
	output.append((w_list[i],result[i], result_Cu[i], result_O[i]))

numpy.savetxt('local_chi.dat',output)

	


