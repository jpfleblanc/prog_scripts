import sys
#uncomment to run on garching
#sys.path.append('/u/jleblanc/software/h5py-2.0.1/base/usr/local/lib64/python2.6/site-packages')
import sys, getopt;
import os, os.path, shutil, distutils.dir_util,numpy,h5py
from numpy import array,average
import re
import math
import resource

#from evalnnsisj import *

#from linreg import linreg

#from collections import namedtuple

#simStructure = namedtuple("simStructure", "density mu sites")

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


def extract_DCA_sigma(filename, clustername, clustersize):
  N=int(clustersize)
  read_file=open(filename, 'r')
  a = numpy.loadtxt(read_file, unpack=True)

  result_w0= imag_selfe(a,0, N)
  result_w1= imag_selfe(a,1, N)

  kx, ky=numpy.loadtxt(open('../../../../cluster_momenta/momenta-'+clustername, 'r'), unpack=True)
  #print(kx,ky)
  
  return kx, ky, result_w0, result_w1

def get_selfe(kx, ky, kxlist, kylist, selfelist):

	for i in range(0, len(kxlist)):
		if kxlist[i]==kx and kylist[i]==ky:
			index=i		
	return selfelist[index]

def nodal_k_index(kxlist,kylist):
	index=1
	for i in range(0, len(kxlist)):
		if abs(kxlist[i]-1.5707)<0.001 and abs(kylist[i]-1.5707)<0.001:
			#print kxlist[i], kylist[i]
			index=i	
#	print "Nodal index is " +str(index)
	return index

def antinodal_k_index(kxlist,kylist):
        index=1
	for i in range(0, len(kxlist)):
		if abs(kxlist[i]-3.14159)<0.001 and abs(kylist[i]-0)<0.001:
#			print kxlist[i], kylist[i]
			index=i	
#	print "AntiNodal index is " +str(index)	
	return index
  

def real_selfe(a, freq, N):

	results=[]

	for j in range(0, 4*int(N)+1):
		if j%2 ==1 and j%4==1:
			#print a[j][freq]
			results.append(a[j][freq])

	return results

def imag_selfe(a, freq, N):

	results=[]

	for j in range(0, 4*int(N)+1):
		#if j%2 ==0 and j>0 and j%4==0:
		if j%2 ==0 and j>0 and j%4==0:
#			print "j is now " + str(j)
#			print a[j][freq]
			results.append(a[j][freq])

	return results



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

def eval():
 
	sitelist=[]
	site_folderlist=[]

	fileslist=[]

	temp_mu_folders=[]
	fig1b=[]

	start_directory=os.getcwd()
	print("Starting in "+start_directory)
	
	files = filter(os.path.isfile, os.listdir('.')) 
	dirs = filter(os.path.isdir, os.listdir('.'))  

	print("Files are " +str(files))
	print("Directories are " +str(dirs))

	for dir_items in dirs:
		print("Directories are "+ dir_items)
		
	for dir_items in dirs:
		if "Betts2D" in dir_items:
			print("Betts folders are " + dir_items)
			if "-ref" not in dir_items and "backup" not in dir_items:
				site_folderlist.append(dir_items)
			sitenum=dir_items[8:-1].strip()			
			sitelist.append(sitenum)	
  	print sitelist	
	sitelist=natural_sort(sitelist)
	site_folderlist=natural_sort(site_folderlist)
	print("Available site folders are ")
	print site_folderlist

	rerun_DF=False
	rerun_inverter=True
	run_anyways=False

	max_number=1000
	current_number=0

# ---------------- Now move into Betts directories

	alldata=[]

	for item in site_folderlist:
		os.chdir(start_directory + "/"+ item)
		print("cd " + start_directory + "/"+ item)
		print("I am in " + os.getcwd())
		temp_mu_folders=filter(os.path.isdir, os.listdir('.'))
		

# --------- check for sim.h5 files
		for folder_item in temp_mu_folders:
			os.chdir(start_directory + "/"+ item+"/"+folder_item)	
			print("I am in " + os.getcwd())
			if os.path.exists(os.getcwd()+"/sim.h5"):
                                f = h5py.File(os.getcwd()+"/sim.h5", 'r')
                                mu=f["/parameters/dictionary/MU"].value
                                site=f["/parameters/dictionary/dca.SITES"].value
                                beta=f["/parameters/dictionary/BETA"].value
                                T=1.0/float(beta)
                                nfreq=f["/parameters/dictionary/NMATSUBARA"].value
                                Uvalue=f["/parameters/dictionary/U"].value
                                tprime=f["/parameters/dictionary/tprime"].value
 

		
				print("I am in " + os.getcwd())
				files_list = [file for file in os.listdir(os.getcwd())]
				sigma_list=[]			
				for file_item in files_list:
					if "selfenergy_" in file_item and "newG0" not in file_item:
						sigma_list.append(file_item)

				if len(sigma_list)>2:
					print len(sigma_list)
					sigma_filename="selfenergy_"+str(len(sigma_list)-1)
					print("Attempting to draw from "+ sigma_filename)
					print (item[:-1])[-2:]			
					kxlist,kylist,w0,w1=extract_DCA_sigma(sigma_filename, item, site)
					print("Nodal and antinodal indices are")
					print (nodal_k_index(kxlist,kylist), antinodal_k_index(kxlist,kylist))		

					awk_command="awk 'FNR>3 {print $1,$"+str(nodal_k_index(kxlist,kylist)*4)+",$"+str(nodal_k_index(kxlist,kylist)*4+1)+",$"+str(antinodal_k_index(kxlist,kylist)*4)+",$"+str(antinodal_k_index(kxlist,kylist)*4+1)+"}' "+sigma_filename+" > n_an_sigma.dat"
					print (awk_command)
					os.system(awk_command)
					nodal_k=nodal_k_index(kxlist,kylist)
					antinodal_k=antinodal_k_index(kxlist,kylist)
					nodal_w0=get_selfe(kxlist[nodal_k], kylist[nodal_k], kxlist, kylist, w0)
					antinodal_w0=get_selfe(kxlist[antinodal_k], kylist[antinodal_k], kxlist, kylist, w0)
					nodal_w1=get_selfe(kxlist[nodal_k], kylist[nodal_k], kxlist, kylist, w1)
					antinodal_w1=get_selfe(kxlist[antinodal_k], kylist[antinodal_k], kxlist, kylist, w1)

					print nodal_w0, nodal_w1, antinodal_w0, antinodal_w1
					
					alldata.append((float(Uvalue),float(T),float(site), 1.0/float(site), float(nodal_w0), float(nodal_w1), float(antinodal_w0), float(antinodal_w1)))


	os.chdir(start_directory)
	numpy.savetxt("dca_sigmas.dat",alldata)
	
			




	

if __name__ == "__main__":
    main(sys.argv[1:])






