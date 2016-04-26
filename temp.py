import sys
#uncomment to run on garching
#sys.path.append('/u/jleblanc/software/h5py-2.0.1/base/usr/local/lib64/python2.6/site-packages')
import sys, getopt;
import os, os.path, shutil, distutils.dir_util,numpy,h5py
from numpy import array,average
import re
import math
import resource

from evalnnsisj import *

from linreg import linreg

from collections import namedtuple

#simStructure = namedtuple("simStructure", "density mu sites")

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


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
			if "-ref" not in dir_items:
				site_folderlist.append(dir_items)
			sitenum=dir_items[8:-1].strip()			
			sitelist.append(sitenum)	
  	print sitelist	
	sitelist=natural_sort(sitelist)
	site_folderlist=natural_sort(site_folderlist)
	print("Available site folders are ")
	print site_folderlist

	

# ---------------- Now move into Betts directories


	for item in site_folderlist:
		os.chdir(start_directory + "/"+ item)
		print("cd " + start_directory + "/"+ item)
		print("I am in " + os.getcwd())
		temp_mu_folders=filter(os.path.isdir, os.listdir('.'))
		

# --------- check for sim.h5 files
		for folder_item in temp_mu_folders:
			if os.path.exists(os.getcwd()+"/"+folder_item+"/sim.h5"):
				#print("sim.h5 exists in folder"+os.getcwd()+"/"+folder_item+"/sim.h5")
				
				
#--------- read in relevant data from sim.h5
				f = h5py.File(os.getcwd()+"/"+folder_item+"/sim.h5", 'r')

				#print folder_item
				#print f["/parameters/MU"].value
				if f["/parameters/MU"].value<=0:

					Sign=(f["/simulation/results/Sign/mean/value"].value)
					if "/simulation/results/density_up_times_sign/mean/value" in f:
						density_mean =(f["/simulation/results/density_up_times_sign/mean/value"].value+f["/simulation/results/density_down_times_sign/mean/value"].value)*0.5
						density_mean = sum(density_mean)/float(len(density_mean))/Sign
						density_mean_err =(f["/simulation/results/density_up_times_sign/mean/error"].value+f["/simulation/results/density_down_times_sign/mean/error"].value)*0.5
						density_mean_err = sum(density_mean_err)/float(len(density_mean_err))/Sign
						doubleoc_mean=(f["/simulation/results/doubleoc_times_sign/mean/value"].value)	
						doubleoc_mean= sum(doubleoc_mean)/float(len(doubleoc_mean))	/Sign
						doubleoc_error=(f["/simulation/results/doubleoc_times_sign/mean/error"].value)
						doubleoc_error=sum(doubleoc_error)/float(len(doubleoc_error))/Sign

						sz2_mean=(f["/simulation/results/Sz_2_times_sign/mean/value"].value)
						sz2_mean=sum(sz2_mean)/float(len(sz2_mean))/Sign
						sz2_error=(f["/simulation/results/Sz_2_times_sign/mean/error"].value)
						sz2_error=sum(sz2_error)/float(len(sz2_error))/Sign
					else:
						density_mean =(f["/simulation/results/density_up/mean/value"].value+f["/simulation/results/density_down/mean/value"].value)*0.5
						density_mean = sum(density_mean)/float(len(density_mean))/Sign
					
						density_mean_err =(f["/simulation/results/density_up/mean/error"].value+f["/simulation/results/density_down/mean/error"].value)*0.5
						density_mean_err = sum(density_mean_err)/float(len(density_mean_err))/Sign
					
#sum(i*i for i in density_mean_err)


						doubleoc_mean=(f["/simulation/results/doubleoc/mean/value"].value)	
						doubleoc_mean= sum(doubleoc_mean)/float(len(doubleoc_mean))	/Sign
						doubleoc_error=(f["/simulation/results/doubleoc/mean/error"].value)
						doubleoc_error=sum(doubleoc_error)/float(len(doubleoc_error))/Sign

						sz2_mean=(f["/simulation/results/Sz_2/mean/value"].value)
						sz2_mean=sum(sz2_mean)/float(len(sz2_mean))/Sign
						sz2_error=(f["/simulation/results/Sz_2/mean/error"].value)
						sz2_error=sum(sz2_error)/float(len(sz2_error))/Sign

					
      					
					mu=f["/parameters/MU"].value
					site=f["/parameters/SITES"].value
					beta=f["/parameters/BETA"].value
					T=1.0/beta
					nfreq=f["/parameters/NMATSUBARA"].value	
					Uvalue=f["/parameters/U"].value	

					if site >15:
						sisjnn, sisjnnerror, nndistance= nnsisj_eval_fromfile(os.getcwd()+"/"+folder_item+"/sim.h5",os.getcwd()+"/"+folder_item+"/ninj_alliterations.dat", 16)#nnsisj_eval(os.getcwd()+"/"+folder_item+"/sim.h5")
					else:
						sisjnn=float('NaN')
						sisjnnerror=float('NaN')
						nndistance=float('NaN')
#------- get energy parameters
					
					files_list = [file for file in os.listdir(os.getcwd()+"/"+folder_item)]
		#			print("Print files list\n")
		#			print files_list
		#			print list_of_files
					
					for file_item in files_list:
						if "selfenergy_" in file_item:
							if "realspace_" not in file_item and "converged_" not in file_item:
								tmpfile=file_item[11:].strip()
								fileslist.append(tmpfile)
					#print("Print files list\n")
					#print fileslist					
					fileslist=natural_sort(fileslist)		
					#print fileslist

					print("Length of fileslist"+ str(len(fileslist)))
#------------ if an iteration completed


					iterationstart=4
				#	if T>2.0:
				#		iterationstart=5
					
					

					if(len(fileslist)>iterationstart):# and site==1
						Iteration=int(fileslist[len(fileslist)-1])
						print("Max iteration was "+str(Iteration))
					
						energy_optionstr=' --siteration '+str(Iteration-iterationstart)+' --niteration '+str(Iteration)+' --directory '+os.getcwd()+ '/'+folder_item+' --nfreq '+str(nfreq)+' --nsite '+str(site)+' --mu '+str(mu)+' --beta '+ str(beta)+' --U '+ str(Uvalue) +' '
						#energy_optionstr=' --siteration '+str(Iteration-(iterationstart-1))+' --niteration '+str(Iteration)+' --directory '+os.getcwd()+ '/'+folder_item+' --nfreq '+str(nfreq)+' --nsite '+str(site)+' --mu '+str(mu)+' --beta '+ str(beta)+' --U '+ str(Uvalue) +' '
						print("\n\n Energy Options "+energy_optionstr+"\n\n")
						


						#comment out - uncomment for fresh energies
						os.system("rm "+os.getcwd()+ "/"+folder_item+"/energy.dat")
#						if os.path.exists(os.getcwd()+"/"+folder_item+"/energy.dat"):
#							if os.path.getmtime(os.getcwd()+ "/"+folder_item+"/energy.dat")> 43000 or os.path.getsize(os.getcwd()+ "/"+folder_item+"/energy.dat")==0:
#								os.system("rm "+os.getcwd()+ "/"+folder_item+"/energy.dat")

						if os.path.exists(os.getcwd()+"/"+folder_item+"/energy.dat"):
							print("Nothing to be done for energy file\n")
							#os.system("rm "+os.getcwd()+ "/"+folder_item+"/energy.dat")	
							#os.system("echo '0 0 0 0 0' > "+os.getcwd()+"/"+folder_item+"/energy.dat")
							os.chdir(os.getcwd()+ '/'+folder_item)
#read in energy lines
							if os.path.getsize(os.getcwd()+'/energy.dat') > 0:
								read_file=open('energy.dat', 'r')
								ekin_mean, ekin_error, epot_mean, epot_error  = numpy.loadtxt(read_file, usecols=(1,2,3,4))
								read_file.close()
							else:
								continue
#							read_file=open('energy.dat', 'r')
#							ekin_mean, ekin_error, epot_mean, epot_error  = numpy.loadtxt(read_file, usecols=(1,2,3,4), unpack=True)
#							read_file.close()
							os.chdir(start_directory + "/"+ item)
						else:
							os.chdir(os.getcwd()+ '/'+folder_item)
							#only update energy if file older than 12 hours
							#os.system("rm "+os.getcwd()+ "/"+folder_item+"/energy.dat")	
							try:
								print "Running energy code"
								os.system("/global/homes/l/leblanc/Hopper/alps_svn/Energy/energy "+ 	energy_optionstr+">> energy.dat")
							except:
								energy_optionstr=' --siteration '+str(4)+' --niteration '+str(7)+' --directory '+os.getcwd()+ '/'+folder_item+' --nfreq '+str(nfreq)+' --nsite '+str(site)+' --mu '+str(mu)+' --beta '+ str(beta)+' --U '+ str(Uvalue) +' '	
								try:
									os.system("/global/homes/l/leblanc/Hopper/alps_svn/Energy/energy "+ 	energy_optionstr+">> energy.dat")
								except:
									pass		

							#os.system("echo '0 0 0 0 0' > "+os.getcwd()+"/"+folder_item+"/energy.dat")
							
#read in energy lines
							if os.path.getsize(os.getcwd()+'/energy.dat') > 0:
								read_file=open('energy.dat', 'r')
								ekin_mean, ekin_error, epot_mean, epot_error  = numpy.loadtxt(read_file, usecols=(1,2,3,4))
								read_file.close()
							else:
								continue

	

							os.chdir(start_directory + "/"+ item)

#1.0/nfreq<<" "<<ekin_mean<<" "<<ekin_error<<" "<<epot_mean<<" "<<epot_error
						
						
#------------ energy ran above

					else:
						Iteration=0 
				
					
					
					

					


					print mu, site 		
#---------- all data in following list	
					if(len(fileslist)>iterationstart):		
						fig1b.append( ( Uvalue, T, mu, ekin_mean+epot_mean, site,  doubleoc_mean, doubleoc_error, ekin_mean, ekin_error, epot_mean, epot_error, density_mean, density_mean_err, sz2_mean, sz2_error, sisjnn, sisjnnerror, Sign))


#---------- delete elements in file lists in loop
			del fileslist[:]
			

	
			





	os.chdir(start_directory)
	datasite=[]

#	sorted(myList, key=lambda x: x[1])
# sort data in list to get what you want 


#create complete database

	database_file=open('database-filling-sisj.dat', 'w+')
	for item in fig1b:
		database_file.write(str(item[0])+" "+str(item[1])+" "+str(item[2])+" "+ str(item[3])+" "+str(item[4])+" "+str(item[5])+" "+str(item[6])+" "+str(item[7])+" "+str(item[8])+" "+str(item[9])+" "+str(item[10])+" "+str(item[11])+" "+str(item[12])+" "+str(item[13])+" "+str(item[14])+" "+str(item[15])+" "+str(item[16])+" "+str(item[17])+"\n")
		


#	want_U=8
#	want_T=1.0
#	want_site=1
#	want_mu=0.0
#	for item in fig1b:
#		if abs(item[0]-want_U)<0.1 and abs(float(item[2]) - want_mu) < 0.001 and abs(float(item[1]) - want_T) < 0.001:
#			datasite.append((item[4], 1.0/item[4], item[3]))
#		
#	datasite=sorted(datasite, key=lambda x: x[1])
#	print datasite
#	

## print to file
#	fig1d_file = open('energiesfor-T'+str(want_T)+'-mu'+str(want_mu)+'.dat', 'w+')
#	for item in datasite:
#		fig1d_file.write(str(item[0])+" "+str(item[1])+" "+str(item[2])+"\n")

	

if __name__ == "__main__":
    main(sys.argv[1:])






