import sys
#uncomment to run on garching
sys.path.append('/u/jleblanc/software/h5py-2.0.1/base/usr/local/lib64/python2.6/site-packages')
import sys, getopt;
import os, os.path, shutil, distutils.dir_util,numpy,h5py
from numpy import array,average
import re
import math
import resource
from numpy import *

from linreg import linreg

from collections import namedtuple

#simStructure = namedtuple("simStructure", "density mu sites")

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


def get_neighbour_dist():

	output=[]
	for i in range (0, 10):
		for j in range (0, i+1):
			
			length=math.sqrt(math.pow(i,2)+ math.pow(j,2))
			#print i, j, length, length*length			
			if length not in output:
				output.append(length)

	output=sorted(output, key=lambda x: x)
	return output


def main(argv):
#  U="8"
#  LATTICE="Betts2D-1A"
#  SITES=1
#  try:                                
#    opts, args = getopt.getopt(argv, "hULs", ["help", "U=", "lattice=","sites="])
#  except getopt.GetoptError:          
#    usage()                         
#    sys.exit(2)                     
#  for opt, arg in opts:
#    if opt in ("-h", "--help"):
#      usage()                     
#      sys.exit()                  
#    elif opt in("-L","--lattice"):
#      LATTICE = arg                 
#    elif opt in ("-U", "--U"):
#      U = arg 
#    elif opt in ("-s", "--sites"):
#      SITES =arg 
  resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))
  eval()

def usage():
  print("call program with -U for U, --sites= for # sites, --lattice= for lattice")

def getninjfromfile(filename, site, itkeep):
	print filename
	
	err=False

	ninj=zeros(4*site*site)
	ninje=zeros(4*site*site)
	count=0

	if os.path.exists(filename):
		read_file=open(filename, 'r')
		ninjlist  = numpy.loadtxt(read_file)
		read_file.close()

	print len(ninjlist)

	itnum= len(ninjlist)/(4*site*site)
	print itnum

	itkeep=itnum
	if (itkeep*site*site*4 > len(ninjlist)):
		#err=True
		#itkeep=itnum
		print "Taking all iterations regardless of request- revert to single iteration"
	else:
		
		print ninjlist[0]

		for x in range (itnum-itkeep, itnum):
			print "X is "+str(x)

	#		for i in range (0, site):
	#			for j in range (0, site):
			for k in range (0, 4*site*site):
				ninj[k]+=ninjlist[k + x*4*site*site ]
			
			

			count +=1

		ninj=ninj/double(count)

		print "Count was "+ str(count)

	


	return ninj, ninje, err



def nnsisj_eval(filename):
 
	f = h5py.File(filename, 'r')

		#print folder_item
		#print f["/parameters/MU"].value

	Sign=(f["/simulation/results/Sign/mean/value"].value)
	if "/simulation/results/ni_nj_times_sign/mean/value" in f:		
		ninj_mean=(f["/simulation/results/ni_nj_times_sign/mean/value"].value)/Sign
		ninj_error=(f["/simulation/results/ni_nj_times_sign/mean/error"].value)/Sign
	else:
		ninj_mean=(f["/simulation/results/ni_nj/mean/value"].value)/Sign
		ninj_error=(f["/simulation/results/ni_nj/mean/error"].value)/Sign
#				ninj_mean=(f["/simulation/results/ni_nj_times_sign/mean/value"].value)
#				ninj_error=(f["/simulation/results/ni_nj_times_sign/mean/error"].value)
		
	mu=f["/parameters/MU"].value
	site=int(f["/parameters/SITES"].value)
	beta=f["/parameters/BETA"].value
	T=1.0/float(beta)
	nfreq=f["/parameters/NMATSUBARA"].value	
	Uvalue=f["/parameters/U"].value	

	
#--------- Get Cluster coordinates

#				os.chdir(os.getcwd()+ '/'+folder_item)

	read_file=open('../../../cluster-coords/ClusterCoordinates'+str(site), 'r')
	label, xval, yval  = numpy.loadtxt(read_file, usecols=(0,1,2), unpack=True)
	read_file.close()
	
	#print label
	#print xval
	#print yval
	if (site==16):	
		ax=4.0
		ay=2.0
		bx=0.0
		by=4.0
	if (site==20):	
		ax=2.0
		ay=4.0
		bx=4.0
		by=-2.0
	if (site==32):
		ax=4.0
		ay=4.0
		bx=4.0
		by=-4.0
	if (site==34):
		ax=3.0
		ay=5.0
		bx=5.0
		by=-3.0
	if (site==50):
		ax=5.0
		ay=5.0
		bx=5.0
		by=-5.0
	if (site==72):
		ax=6.0
		ay=6.0
		bx=6.0
		by=-6.0
	topval=6

	nntest=zeros((int(site),int(site),topval)).astype(int)
	#print nntest
	#print nntest[1][1]



#------------------------------		
	distance=get_neighbour_dist()
	#print "Distance list length"
	#print len(distance)

	
	length1=zeros(topval)
	length2=zeros(topval)
	length3=zeros(topval)
	length4=zeros(topval)
	length5=zeros(topval)
	length6=zeros(topval)
	length7=zeros(topval)
	length8=zeros(topval)
	length9=zeros(topval)

	



	for x in range (0, topval):
		for i in range (0, int(site)):
			counter=0
			for j in range (0, int(site)):
				length1[x]=math.fabs(math.sqrt( math.pow((xval[j]-xval[i]),2) + math.pow((yval[j]-yval[i]),2))-distance[x])
				length2[x]=math.fabs(math.sqrt( math.pow((xval[j]+ax-xval[i]),2) + math.pow((yval[j]+ay-yval[i]),2))-distance[x])
				length3[x]=math.fabs(math.sqrt( math.pow((xval[j]-ax-xval[i]),2) + math.pow((yval[j]-ay-yval[i]),2))-distance[x])
				length4[x]=math.fabs(math.sqrt( math.pow((xval[j]+bx-xval[i]),2) + math.pow((yval[j]+by-yval[i]),2))-distance[x])
				length5[x]=math.fabs(math.sqrt( math.pow((xval[j]-bx-xval[i]),2) + math.pow((yval[j]-by-yval[i]),2))-distance[x])
				length6[x]=math.fabs(math.sqrt( math.pow((xval[j]+ax+bx-xval[i]),2) + math.pow((yval[j]+ay+by-yval[i]),2))-distance[x])
				length7[x]=math.fabs(math.sqrt( math.pow((xval[j]-ax-bx-xval[i]),2) + math.pow((yval[j]-ay-by-yval[i]),2))-distance[x])
				length8[x]=math.fabs(math.sqrt( math.pow((xval[j]+ax-bx-xval[i]),2) + math.pow((yval[j]+ay-by-yval[i]),2))-distance[x])
				length9[x]=math.fabs(math.sqrt( math.pow((xval[j]-ax+bx-xval[i]),2) + math.pow((yval[j]-ay+by-yval[i]),2))-distance[x])

				if (i ==j and i==0 and x==0):
					print "HERE"
					print length1[0]
				#print length1
				if (length1[x] < 0.01 or length2[x] <0.01 or length3[x] <0.01 or length4[x] <0.01 or length5[x] <0.01 or length6[x] <0.01 or length7[x] <0.01 or length8[x] < 0.01 or length9[x] < 0.01 ):
					counter+=1
					nntest[i][j][x]=1



		print nntest[1][1][0]

	

		print "There were "+str(counter)+" nearest neighbours at distance"+str(distance[x])
	#	if (counter != 4):
	#		print "Something wasn't found! ABORT!!!"

#-------------------------------
#  now have the ninj's AND their nearest neighbour choices

		nuu=zeros((site,site))
		nud=zeros((site,site))
		ndu=zeros((site,site))
		ndd=zeros((site,site))
		nuue=zeros((site,site))
		nude=zeros((site,site))
		ndue=zeros((site,site))
		ndde=zeros((site,site))
		sz=zeros(topval)
		sze=zeros(topval)
		sznew=zeros(topval)
		totalcount=zeros(topval)

		for i in range (0, site):
			for j in range (0, site):
				nuu[i][j]=ninj_mean[4*site*i+4*j]
				nud[i][j]=ninj_mean[4*site*i+4*j+1]
				ndu[i][j]=ninj_mean[4*site*i+4*j+2]
				ndd[i][j]=ninj_mean[4*site*i+4*j+3]

				nuue[i][j]=ninj_error[4*site*i+4*j]
				nude[i][j]=ninj_error[4*site*i+4*j+1]
				ndue[i][j]=ninj_error[4*site*i+4*j+2]
				ndde[i][j]=ninj_error[4*site*i+4*j+3]


		for x in range (0,topval):
			#print "X is "+str(x)
			for i in range (0, site):
				for j in range (0, site):
				
					if (nntest[i][j][x]==1):
						sz[x]+=(nuu[i][j]-nud[i][j]-ndu[i][j]+ndd[i][j])
#							sze+=(nuue[i][j]*nuue[i][j]+nude[i][j]*nude[i][j]+ndue[i][j]*ndue[i][j]+ndde[i][j]*ndde[i][j])
						totalcount[x]+=1
				#		nntest[i][j][x]=-1
				#		nntest[j][i][x]=-1
						#print sz


		
		

#				sz=sz*sz2_mean/4/site
			sz[x]=sz[x]/(totalcount[x])
			for i in range (0, site):
				for j in range (0, site):
			
					if (nntest[i][j][x]==1):
						sznew[x]=(nuu[i][j]-nud[i][j]-ndu[i][j]+ndd[i][j])
						sze[x]+=math.pow(sznew[x]-sz[x],2)
						#print sz, sznew
					
				#		nntest[i][j][x]=1
				#		nntest[j][i][x]=1
						#print sz


		
			sze[x]=math.sqrt(sze[x]/(totalcount[x]))
#				sze= math.sqrt(2.0*math.pow(sze/4/site/sz,2)+math.pow(sz2_error/sz2_mean,2))*sz
# extra division by 5 to deal with double counting of each connection. 1 for the center, 4 for when you're on the outside


		#print "Value for sz is \n"
		#print sz, sze, sz2_mean, totalcount		


	print "Returning nn values "
	print sz[1], sze[1], distance[1]

	return sz[1], sze[1], distance[1]
	
def nnsisj_eval_fromfile(filename, ninjfile,itkeep):
 
	f = h5py.File(filename, 'r')

		#print folder_item
		#print f["/parameters/MU"].value

	Sign=(f["/simulation/results/Sign/mean/value"].value)
	site=f["/parameters/SITES"].value
	err=False
	if "/simulation/results/ni_nj_times_sign/mean/value" in f:
		if os.path.exists(ninjfile):
			print "Reading ninj file"
			ninj_mean, ninj_error, err = getninjfromfile(ninjfile, site, itkeep)	
			print err	
		if os.path.exists(ninjfile)==False:
			print "NOT Reading ninj which is at " + ninjfile
			ninj_mean=(f["/simulation/results/ni_nj_times_sign/mean/value"].value)/Sign
			ninj_error=(f["/simulation/results/ni_nj_times_sign/mean/error"].value)/Sign
	else:
		if os.path.exists(ninjfile):
			print "Reading ninj file which is at " + ninjfile
			ninj_mean, ninj_error, err = getninjfromfile(ninjfile, site, itkeep)		
		if os.path.exists(ninjfile)==False:
			print "NOT Reading ninj which is at " + ninjfile
			ninj_mean=(f["/simulation/results/ni_nj/mean/value"].value)/Sign
			ninj_error=(f["/simulation/results/ni_nj/mean/error"].value)/Sign
#				ninj_mean=(f["/simulation/results/ni_nj_times_sign/mean/value"].value)
#				ninj_error=(f["/simulation/results/ni_nj_times_sign/mean/error"].value)
		
	mu=f["/parameters/MU"].value
	site=f["/parameters/SITES"].value
	beta=f["/parameters/BETA"].value
	T=1.0/beta
	nfreq=f["/parameters/NMATSUBARA"].value	
	Uvalue=f["/parameters/U"].value	

	
#--------- Get Cluster coordinates

#				os.chdir(os.getcwd()+ '/'+folder_item)

	read_file=open('../../cluster-coords/ClusterCoordinates'+str(site), 'r')
	label, xval, yval  = numpy.loadtxt(read_file, usecols=(0,1,2), unpack=True)
	read_file.close()
	
	#print label
	#print xval
	#print yval
	if (site==16):	
		ax=4.0
		ay=2.0
		bx=0.0
		by=4.0
	if (site==20):	
		ax=2.0
		ay=4.0
		bx=4.0
		by=-2.0
	if (site==32):
		ax=4.0
		ay=4.0
		bx=4.0
		by=-4.0
	if (site==34):
		ax=3.0
		ay=5.0
		bx=5.0
		by=-3.0
	if (site==50):
		ax=5.0
		ay=5.0
		bx=5.0
		by=-5.0

	topval=6

	nntest=zeros((site,site,topval)).astype(int)
	#print nntest
	#print nntest[1][1]



#------------------------------		
	distance=get_neighbour_dist()
	#print "Distance list length"
	#print len(distance)

	
	length1=zeros(topval)
	length2=zeros(topval)
	length3=zeros(topval)
	length4=zeros(topval)
	length5=zeros(topval)
	length6=zeros(topval)
	length7=zeros(topval)
	length8=zeros(topval)
	length9=zeros(topval)

	



	for x in range (0, topval):
		for i in range (0, site):
			counter=0
			for j in range (0, site):
				length1[x]=math.fabs(math.sqrt( math.pow((xval[j]-xval[i]),2) + math.pow((yval[j]-yval[i]),2))-distance[x])
				length2[x]=math.fabs(math.sqrt( math.pow((xval[j]+ax-xval[i]),2) + math.pow((yval[j]+ay-yval[i]),2))-distance[x])
				length3[x]=math.fabs(math.sqrt( math.pow((xval[j]-ax-xval[i]),2) + math.pow((yval[j]-ay-yval[i]),2))-distance[x])
				length4[x]=math.fabs(math.sqrt( math.pow((xval[j]+bx-xval[i]),2) + math.pow((yval[j]+by-yval[i]),2))-distance[x])
				length5[x]=math.fabs(math.sqrt( math.pow((xval[j]-bx-xval[i]),2) + math.pow((yval[j]-by-yval[i]),2))-distance[x])
				length6[x]=math.fabs(math.sqrt( math.pow((xval[j]+ax+bx-xval[i]),2) + math.pow((yval[j]+ay+by-yval[i]),2))-distance[x])
				length7[x]=math.fabs(math.sqrt( math.pow((xval[j]-ax-bx-xval[i]),2) + math.pow((yval[j]-ay-by-yval[i]),2))-distance[x])
				length8[x]=math.fabs(math.sqrt( math.pow((xval[j]+ax-bx-xval[i]),2) + math.pow((yval[j]+ay-by-yval[i]),2))-distance[x])
				length9[x]=math.fabs(math.sqrt( math.pow((xval[j]-ax+bx-xval[i]),2) + math.pow((yval[j]-ay+by-yval[i]),2))-distance[x])

				if (i ==j and i==0 and x==0):
					print "HERE"
					print length1[0]
				#print length1
				if (length1[x] < 0.01 or length2[x] <0.01 or length3[x] <0.01 or length4[x] <0.01 or length5[x] <0.01 or length6[x] <0.01 or length7[x] <0.01 or length8[x] < 0.01 or length9[x] < 0.01 ):
					counter+=1
					nntest[i][j][x]=1



		print nntest[1][1][0]

	

		print "There were "+str(counter)+" nearest neighbours at distance"+str(distance[x])
	#	if (counter != 4):
	#		print "Something wasn't found! ABORT!!!"

#-------------------------------
#  now have the ninj's AND their nearest neighbour choices

		nuu=zeros((site,site))
		nud=zeros((site,site))
		ndu=zeros((site,site))
		ndd=zeros((site,site))
		nuue=zeros((site,site))
		nude=zeros((site,site))
		ndue=zeros((site,site))
		ndde=zeros((site,site))
		sz=zeros(topval)
		sze=zeros(topval)
		sznew=zeros(topval)
		totalcount=zeros(topval)

		for i in range (0, site):
			for j in range (0, site):
				nuu[i][j]=ninj_mean[4*site*i+4*j]
				nud[i][j]=ninj_mean[4*site*i+4*j+1]
				ndu[i][j]=ninj_mean[4*site*i+4*j+2]
				ndd[i][j]=ninj_mean[4*site*i+4*j+3]

				nuue[i][j]=ninj_error[4*site*i+4*j]
				nude[i][j]=ninj_error[4*site*i+4*j+1]
				ndue[i][j]=ninj_error[4*site*i+4*j+2]
				ndde[i][j]=ninj_error[4*site*i+4*j+3]


		for x in range (0,topval):
			#print "X is "+str(x)
			for i in range (0, site):
				for j in range (0, site):
				
					if (nntest[i][j][x]==1):
						sz[x]+=(nuu[i][j]-nud[i][j]-ndu[i][j]+ndd[i][j])
#							sze+=(nuue[i][j]*nuue[i][j]+nude[i][j]*nude[i][j]+ndue[i][j]*ndue[i][j]+ndde[i][j]*ndde[i][j])
						totalcount[x]+=1
				#		nntest[i][j][x]=-1
				#		nntest[j][i][x]=-1
						#print sz


		
		

#				sz=sz*sz2_mean/4/site
			sz[x]=sz[x]/(totalcount[x])
			for i in range (0, site):
				for j in range (0, site):
			
					if (nntest[i][j][x]==1):
						sznew[x]=(nuu[i][j]-nud[i][j]-ndu[i][j]+ndd[i][j])
						sze[x]+=math.pow(sznew[x]-sz[x],2)
						#print sz, sznew
					
				#		nntest[i][j][x]=1
				#		nntest[j][i][x]=1
						#print sz


		
			sze[x]=math.sqrt(sze[x]/(totalcount[x]))
#				sze= math.sqrt(2.0*math.pow(sze/4/site/sz,2)+math.pow(sz2_error/sz2_mean,2))*sz
# extra division by 5 to deal with double counting of each connection. 1 for the center, 4 for when you're on the outside


		#print "Value for sz is \n"
		#print sz, sze, sz2_mean, totalcount		


	print "Returning nn values "
	print sz[1], sze[1], distance[1]

	return sz[1], sze[1], distance[1]

	

if __name__ == "__main__":
    main(sys.argv[1:])






