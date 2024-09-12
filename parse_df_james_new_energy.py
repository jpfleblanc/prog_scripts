# An example of parsing df data
import h5py
import numpy as np
import os, os.path, shutil, distutils.dir_util
from numpy import pi

from scipy import special




def main(fname = "output.h5", verbosity = 1):
    h5file = h5py.File(fname, "r")
    data = h5file["df"]
    # import lattice gf
    (grids, glat) = read_hdf5(data["glat"])
    # extract grid of Matsubara values (it is stored as a complex number, so h5py imports into 
    wgrid = grids[0].copy()[:,1]
    # extract grid of k-points (in one of the dimensions)
    kgrid = grids[1].copy()
    print "Matsubara grid =", wgrid if verbosity > 1 else None 
    print "BZ mesh =", kgrid if verbosity > 1 else None 

    # extract beta from Matsubara spacing
    beta = 2.0*pi/(wgrid[1]-wgrid[0])
    print "beta =", beta if verbosity > 0 else None
    
    # find the Matsubara frequency, closest to zero
    w0 = find_nearest_index(wgrid, pi/beta)

    # read self-energy
    (grids, sigma_lat) = read_hdf5(data["sigma_lat"])




    print "Sigma testing "
    #print sigma_lat[0][0][0], glat[0][0][0]   # does element wise multiplication
    #print sigma_lat[0][0][1][0], sigma_lat[0][0][1][1]  # sigma_[kx][ky][w][0 or 1 for real and imaginary]
    print sigma_lat[0][0][0]*glat[0][0][0]
    print (sigma_lat[0][0][0]*glat[0][0][0]).sum()

    n_kpoints = len(data["sigma_lat"]["grids"]["1"]["values"])
    n_wpoints = len(data["sigma_lat"]["grids"]["0"]["values"])
    print n_kpoints, n_wpoints


    sigma_lat=sigma_lat.view(complex)
    glat=glat.view(complex)
    #print sigma_lat[0][0][0], glat[0][0][0]

    write_readable(sigma_lat, glat, n_kpoints, n_wpoints, wgrid)
    write_plotable(glat, n_kpoints, n_wpoints, wgrid)

    

   
    sigma=sigma_lat.copy()
    g=glat.copy()

    I1=0
    I2=0
    

    complex_i=0+1j

    imag_wgrid=wgrid.copy()
    imag_wgrid=imag_wgrid*complex_i


    sigma_slice=[]
    g_slice=[]

    green_c1 = [[0 for x in range(n_kpoints)] for x in range(n_kpoints)] 
    green_c2 = [[0 for x in range(n_kpoints)] for x in range(n_kpoints)] 
    green_c3 = [[0 for x in range(n_kpoints)] for x in range(n_kpoints)] 

    sigma_c0 = [[0 for x in range(n_kpoints)] for x in range(n_kpoints)] 
    sigma_c1 = [[0 for x in range(n_kpoints)] for x in range(n_kpoints)] 

    density_matrix=[[0 for x in range(n_kpoints)] for x in range(n_kpoints)] 
    tail_matrix=[[0 for x in range(n_kpoints)] for x in range(n_kpoints)] 



    high_freq_int= beta*beta* special.polygamma(1, 0.5+n_wpoints/2.0)/4/np.pi/np.pi

    density=0.0
    density_2=0.0
    tail=0.0

## Global skip for skipping momenta

    global_skip=1


    for kx in range (n_kpoints):
      for ky in range (n_kpoints):
        if kx%global_skip==0 and ky%global_skip==0:
         # print kx, ky
          green_c1[kx][ky]=1.0
          green_c2[kx][ky]=np.real(g[n_wpoints-1][kx][ky])*np.real(imag_wgrid[n_wpoints-1]*imag_wgrid[n_wpoints-1]   )
          green_c3[kx][ky]= -  ( np.imag(g[n_wpoints-1][kx][ky]) - np.imag(1.0/imag_wgrid[n_wpoints-1])) *np.imag( imag_wgrid[n_wpoints-1]*imag_wgrid[n_wpoints-1]*imag_wgrid[n_wpoints-1]  )    
        #print green_c2

       
   # print 'Constants'
    #print green_c1, green_c2, green_c3



    for kx in range (n_kpoints):
      for ky in range (n_kpoints):
        for w in range (n_wpoints/2, n_wpoints):  
          if kx%global_skip==0 and ky%global_skip==0:
	 # multiply by extra 2 for spin flavour
            I2+=-2.0*np.real(sigma[w][kx][ky]*g[w][kx][ky])/pow(len(kgrid)/global_skip,2)/beta*2.0  
            I1+= 2.0*(-1 + abs(wgrid[w])*abs(np.imag(g[w][kx][ky])))/pow(len(kgrid)/global_skip,2)/beta *2.0          #np.abs(wgrid[w]* np.imag(g[w][kx][ky])/pow(len(kgrid),2)/beta)-1.0

# compute density

    print "About to compute the density"
   # print green_c2

    for kx in range (n_kpoints):
      for ky in range (n_kpoints):
        for w in range (n_wpoints/2, n_wpoints): 
          if kx%global_skip==0 and ky%global_skip==0: 
          #print w
            density_matrix[kx][ky]+=2.0*np.real(g[w][kx][ky])/beta  #*2.0 # not sure why this 2 was here
          #print np.sign(g[w][kx][ky])

            #density_2+=np.abs(np.real(g[w][kx][ky]))/beta/pow(len(kgrid)/global_skip,2)

          #print np.abs(np.real(g[w][kx][ky]))/beta
        density_matrix[kx][ky]-= 2.0*high_freq_int * green_c2[kx][ky]/beta
        tail_matrix[kx][ky]-= 2.0*high_freq_int * green_c2[kx][ky]/beta
       # print 2.0*high_freq_int * green_c2[kx][ky]/beta


    for kx in range (n_kpoints):
      for ky in range (n_kpoints):   
        if kx%global_skip==0 and ky%global_skip==0:
          density+= density_matrix[kx][ky]/pow(len(kgrid)/global_skip,2)
          tail+= tail_matrix[kx][ky]/pow(len(kgrid)/global_skip,2)
        #  print density
    print "Density is "
    print density
    print "DMFT density was"
    if os.path.exists("../../sim.h5"):
      f = h5py.File("../../sim.h5", 'r')
      density_mean =(f["/simulation/results/density_up/mean/value"].value+f["/simulation/results/density_down/mean/value"].value)*0.5
      density_mean = sum(density_mean)/float(len(density_mean))
    print density_mean


    print "Tail part is "
    print tail



    U_value=2.0#12.0
    #density=1.0

    for kx in range (n_kpoints):
      for ky in range (n_kpoints):
        if kx%global_skip==0 and ky%global_skip==0:
          sigma_c0[kx][ky]= U_value*(2.0*density-0.5)#-U_value*(density)#U_value*(density-0.5)
          sigma_c1[kx][ky]= -U_value*U_value*2.0*density*(1.0-2.0*density)#-U_value*U_value*(0.5+density)*(0.5-density)#-U_value*U_value*density*(1.0-density)


    sigma_cor1=0.
    sigma_cor2=0.
    gw_1=0.
    for kx in range (n_kpoints):
      for ky in range (n_kpoints):
        if kx%global_skip==0 and ky%global_skip==0:
          sigma_cor1+=2.0/pow(len(kgrid)/global_skip,2)/beta *( green_c1[kx][ky]*sigma_c1[kx][ky]*high_freq_int   )*2.0
          sigma_cor2-=2.0/pow(len(kgrid)/global_skip,2)/beta *( green_c2[kx][ky]*sigma_c0[kx][ky]*high_freq_int   )*2.0
        
          gw_1-=2.0/pow(len(kgrid)/global_skip,2)/beta *( green_c3[kx][ky]*high_freq_int      )


    for w in range (n_wpoints):
      sigma_slice.append((wgrid[w], np.real(sigma[w][0][0])[0], np.imag(sigma[w][0][0])[0]))


    #print sigma_slice[128]

    np.savetxt('sigma_pi0.dat', sigma_slice)



   
       
    #print sigma[0][0][1]

    print "I1 and I2"
    print I1, I2
    print sigma_cor1, sigma_cor2, gw_1, high_freq_int, density, density_2
    I2-= sigma_cor1 + sigma_cor2
    I1+= gw_1

    potential_energy =  U_value/4.0 - I2/2.0 #+ gw_1/2.0
    kinetic_energy= (I1+I2)#2.0*(I1 -I2) 
    hartree_part=U_value*density/2.0
    #hartree_shift=-U_value*(density-0.5)


    print "Potential energy "+ str(potential_energy +hartree_part)
    print "kinetic energy " +str(kinetic_energy-hartree_part)
    print "Hartree Part " +str(hartree_part)
    print "Sum " +str(potential_energy+kinetic_energy )

    print "Corrections "
    print sigma_cor1, sigma_cor2, gw_1, high_freq_int, hartree_part, density, density_2

    #print "Adding terms"
    #print potential_energy, gw_1, potential_energy+gw_1/2.0


   # print "Tr[\Sigma * G] = ", potential_energy, (sigma_lat*glat).sum()/pow(len(kgrid),2)/beta

    
def read_hdf5(group):
    ''' read gridobject from hdf5 '''
    data = group["data"]
    ngrids = len(group["grids"].keys())
    grids = [np.array(group["grids"][str(i)]["values"][()]) for i in range(ngrids)]
    return (grids, np.array(data))
def find_nearest_index(array,value):
    idx = (abs(array-value)).argmin()
    return idx 
def find_nearest(array,value):
    return array[find_nearest_index(array,value)]

def write_readable(sigma, g_w, n_k, n_w, wgrid):

    print "Writing E_file for checking"

    print n_k, n_w
    print sigma[n_w-1][n_k-1][n_k-1]


    greal_file=open("PARSED_Greal_1", "w+")
    gimag_file=open("PARSED_Gimag_1", "w+")
    sigma_file=open("PARSED_SIGMA_1", "w+")
    for w in range (n_w/2, n_w):
      print w
      print np.real(g_w[w][0][0])
      write_string=str(wgrid[w])+" "
      write_string2=str(wgrid[w])+" "
      write_string_sigma=str(wgrid[w])+" "
      for kx in range (n_k):
        for ky in range (n_k):
          write_string+=" "+str(np.real(g_w[w][kx][ky])[0])
          write_string2+=" "+" "+str(np.imag(g_w[w][kx][ky])[0])
          write_string_sigma+=" "+str(np.real(sigma[w][kx][ky])[0])+" "+str(np.imag(sigma[w][kx][ky])[0])
     # print write_string
      greal_file.write(write_string+"\n")
      gimag_file.write(write_string+"\n")
      sigma_file.write(write_string_sigma+"\n")

    #for kx in range (n_kpoints):
     # for ky in range (n_kpoints):
         
def write_plotable(g_w, n_k, n_w, wgrid):

    g_file=open("Plotable.dat","w+")
    for kx in range (n_k):
        for ky in range (n_k):
          write_string=str(kx)+" "+str(ky)+" "+str(np.real(g_w[n_k/2][kx][ky])[0])
          g_file.write(write_string+"\n")



if __name__ == "__main__":
    main()
