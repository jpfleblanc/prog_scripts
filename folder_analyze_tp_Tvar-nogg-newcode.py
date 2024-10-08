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
	temp_mu_folders_filtered=[]
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
	rerun_inverter=False
	run_anyways=False

	max_number=1000
	current_number=0

# ---------------- Now move into Betts directories


	for item in site_folderlist:
		os.chdir(start_directory + "/"+ item)
		print("cd " + start_directory + "/"+ item)
		print("I am in " + os.getcwd())
		temp_mu_folders=filter(os.path.isdir, os.listdir('.'))
		for temp_item in temp_mu_folders:
			if "-ref" not in dir_items and "backup" not in temp_item:
				temp_mu_folders_filtered.append(temp_item)
		
		print 'Folders are '
		print temp_mu_folders_filtered
# --------- check for sim.h5 files
		for folder_item in temp_mu_folders_filtered:
			
			print "folder item is "+ folder_item
			os.chdir(start_directory + "/"+ item+"/"+folder_item+"/vertex_run")
			if os.path.exists(os.getcwd()+"/sim.h5"):
				f = h5py.File(os.getcwd()+"/sim.h5", 'r')
				mu=f["/parameters/MU"].value
				site=f["/parameters/dca.SITES"].value
				beta=f["/parameters/BETA"].value
				T=1.0/float(beta)
				nfreq=f["/parameters/NMATSUBARA"].value	
				Uvalue=f["/parameters/U"].value	
				tprime=f["/parameters/tprime"].value


			print("I am in " + os.getcwd())
			print("Directory is "+ start_directory + "/"+ item+"/"+folder_item+"/vertex_run" +"/run_DF_nogg/sigma_output_nodal.dat")
			print("Should I be running in here? "+ str(os.path.exists(start_directory + "/"+ item+"/"+folder_item+"/vertex_run" +"/run_DF_nogg/sigma_output_nodal.dat")))

			DF_running_path=os.getcwd()+"/runningDF.dat"
			
			if True:#os.path.exists(DF_running_path)==False:
				os.system("echo 'blah'> runningDF.dat")
				if os.path.exists(start_directory + "/"+ item+"/"+folder_item+"/vertex_run" +"/run_DF_nogg/output.h5") == False or run_anyways:
					current_number=current_number+1
					if (current_number>max_number):
						print("Hit max run, exiting")
						exit()
					# check if inverter should be run
					if os.path.exists(os.getcwd()+"/vert_F_phpp")==False or rerun_inverter==True:
						os.system("sh /home/jpfleblanc/working/prog_scripts/run_inverter_inplace_newcode.sh")
					# check if run_DF folder exists	
					if os.path.exists(os.getcwd()+"/run_DF_nogg")==False:
						os.system("mkdir run_DF_nogg")
					os.chdir(os.getcwd()+"/run_DF_nogg")	
				#	print("I am in " + os.getcwd())	
					# check if qmc_output has been made
					if os.path.exists(os.getcwd()+"/qmc_output.h5")==False:
						options_str="--vertex ../vert_F_phpp --gw ../../G_omega_17 --sigma ../../selfenergy_17  --mu "+str(mu)
						os.system("python $HOME/alps_git/scripts/dmft_to_opendf/parse_alpscore_data.py "+ options_str)
					# run_DF
					if os.path.exists(os.getcwd()+"/output.h5")==False or rerun_DF==True:
						#os.system("sh ../../../../../prog_runs_scripts/run_DF.sh")
						print "Calculation string is"
						run_string="$HOME/alps_core/opendf/install/bin/hub_df_square_nnn --input qmc_output.h5  --df_sc_cutoff 1.0e-8 --df_sc_iter 1200 --df_sc_mix 0.2 --fluct_diag 0 --nbosonic 32 --add_lattice_bubble 0 --mu "+str(mu) +" --tp "+str(tprime) +" --resume 1"
						print run_string

						os.system(run_string)				

					os.system("python /home/jpfleblanc/working/prog_scripts/slice_spinwave_script.py "+str(beta) )
				os.system("rm "+DF_running_path)



	
			




	

if __name__ == "__main__":
    main(sys.argv[1:])






