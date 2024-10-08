# An example of parsing df data
import h5py
import numpy as np
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


    # Read fluct_diag
    

    (grids, sigma_lat_pz) = read_hdf5(data["fluct_diag/sigma_lat_3.14159_0"])
    (grids, sigma_lat_p2p2) = read_hdf5(data["fluct_diag/sigma_lat_1.5708_1.5708"])
    bose_grid= grids[0].copy()[:,1]
    fermi_grid= grids[1].copy()[:,1]
    qx_grid= grids[2].copy()
    qy_grid= grids[3].copy()

    
    
 

  #  print "TESTING GRIDS"
   # print bose_grid[0], fermi_grid[0], qx_grid[1]  
    #print (sigma_lat_pz[len(bose_grid)/2][len(fermi_grid)/2][0][0])


    n_kpoints = len(data["sigma_lat"]["grids"]["1"]["values"])
    n_wpoints = len(data["sigma_lat"]["grids"]["0"]["values"])
 #   print n_kpoints, n_wpoints


    sigma_lat=sigma_lat.view(complex)
    glat=glat.view(complex)
    #print sigma_lat[0][0][0], glat[0][0][0]

    write_readable(sigma_lat, glat, n_kpoints, n_wpoints, wgrid)
    write_plotable(glat, n_kpoints, n_wpoints, wgrid)

    

   
    sigma=sigma_lat.copy()
    g=glat.copy()


 #   print kgrid[0]

#############
    sigma_collect=[]
    kxwanted=0.0
    kywanted=3.14159
    for kx in range (n_kpoints):
      for ky in range (n_kpoints):
        for w in range(n_wpoints/2, n_wpoints):
          if abs(kxwanted-kgrid[kx])<0.001 and abs(kywanted-kgrid[ky])<0.001: 
        #    print kx, ky, kgrid[kx], kgrid[ky]
	    sigma_collect.append((2*np.pi/beta*(w-n_wpoints/2+0.5), kgrid[kx], kgrid[ky], np.real(sigma[w][kx][ky])[0], np.imag(sigma[w][kx][ky])[0]))


    np.savetxt("sigma_output_antinodal.dat", sigma_collect)


    sigma_collect=[]
    kxwanted=3.14159265/2.0
    kywanted=3.14159265/2.0
    for kx in range (n_kpoints):
      for ky in range (n_kpoints):
        for w in range(n_wpoints/2, n_wpoints):
          if abs(kxwanted-kgrid[kx])<0.001 and abs(kywanted-kgrid[ky])<0.001: 
	    sigma_collect.append((2*np.pi/beta*(w-n_wpoints/2+0.5), kgrid[kx], kgrid[ky], np.real(sigma[w][kx][ky])[0], np.imag(sigma[w][kx][ky])[0]))


    np.savetxt("sigma_output_nodal.dat", sigma_collect)


#############

# write plottable fluct_diag file
    diag_collect=[]
    
    for qx in range (len(qx_grid)):
      for qy in range (n_kpoints):
        diag_collect.append((qx_grid[qx], qy_grid[qy], (sigma_lat_pz[len(bose_grid)/2][len(fermi_grid)/2][qx][qy])[1], (sigma_lat_p2p2[len(bose_grid)/2][len(fermi_grid)/2][qx][qy])[1]))


    np.savetxt("fluct_diag_node-antinode.dat", diag_collect)

# write plottable fluct_diag file
    delta_collect=[]
    
    fluct_sum_pz=np.zeros(len(fermi_grid))
    fluct_sum_p2p2=np.zeros(len(fermi_grid))

    fluct_sum_qxqy_pz=np.zeros((len(fermi_grid), len(bose_grid)))
    fluct_sum_qxqy_p2p2=np.zeros((len(fermi_grid), len(bose_grid)))

    fluct_sum_Omega_pz=np.zeros((len(fermi_grid), len(qx_grid), len(qx_grid)))
    fluct_sum_Omega_p2p2=np.zeros((len(fermi_grid), len(qx_grid), len(qx_grid)))

  #  print len(fluct_sum)

    for qx in range (0,len(qx_grid)):
      for qy in range (0,len(qx_grid)):
        for fermi in range(0, len(fermi_grid)):
	  for bose in range(0, len(bose_grid)):
            delta_collect.append((fermi_grid[fermi], qx_grid[qx], qy_grid[qy], bose_grid[bose],  (sigma_lat_pz[bose][fermi][qx][qy])[1], (sigma_lat_p2p2[bose][fermi][qx][qy])[1]))

# summation lines for full summation
            fluct_sum_pz[fermi]=fluct_sum_pz[fermi]+(sigma_lat_pz[bose][fermi][qx][qy])[1]
            fluct_sum_p2p2[fermi]=fluct_sum_p2p2[fermi]+(sigma_lat_p2p2[bose][fermi][qx][qy])[1]
## summation lines for qx qy summation

            fluct_sum_qxqy_pz[fermi][bose]=fluct_sum_qxqy_pz[fermi][bose] + (sigma_lat_pz[bose][fermi][qx][qy])[1]
            fluct_sum_qxqy_p2p2[fermi][bose]=fluct_sum_qxqy_p2p2[fermi][bose] + (sigma_lat_p2p2[bose][fermi][qx][qy])[1]

# summation lines for Omega summation 

            fluct_sum_Omega_pz[fermi][qx][qy]= fluct_sum_Omega_pz[fermi][qx][qy] + (sigma_lat_pz[bose][fermi][qx][qy])[1]
            fluct_sum_Omega_p2p2[fermi][qx][qy]= fluct_sum_Omega_p2p2[fermi][qx][qy] + (sigma_lat_p2p2[bose][fermi][qx][qy])[1]


## write full file
    np.savetxt("full_fluct_diag_file.dat", delta_collect)

# write full sum
    fluct_sum=[]
    for fermi in range(0,len(fermi_grid)):
      fluct_sum.append((fermi, fermi_grid[fermi], fluct_sum_pz[fermi], fluct_sum_p2p2[fermi] ))


    np.savetxt("fluct_sum_DFONLY.dat", fluct_sum)

# write qxqy sum

    fluct_qxqysum=[]
    for fermi in range(0,len(fermi_grid)):
      for bose in range(0, len(bose_grid)):
        fluct_qxqysum.append((fermi, fermi_grid[fermi], bose, bose_grid[bose], fluct_sum_qxqy_pz[fermi][bose], fluct_sum_qxqy_p2p2[fermi][bose]))

    np.savetxt("fluct_sum_qxqy_DFONLY.dat", fluct_qxqysum)

# write Omega sum

    fluct_Omega_sum=[]
    for fermi in range(0,len(fermi_grid)):
      for qx in range(0, len(qx_grid)):
        for qy in range(0, len(qx_grid)):
          fluct_Omega_sum.append((fermi, fermi_grid[fermi], qx_grid[qx], qx_grid[qy], fluct_sum_Omega_pz[fermi][qx][qy], fluct_sum_Omega_p2p2[fermi][qx][qy]))

    np.savetxt("fluct_sum_Omega_DFONLY.dat", fluct_Omega_sum)


###

    sigma_slice=[]
    for w in range (n_wpoints):
      sigma_slice.append((wgrid[w], kgrid[0], kgrid[8], np.real(sigma[w][0][8])[0], np.imag(sigma[w][0][8])[0]))


    #print sigma_slice[128]

    np.savetxt('sigma_pi0.dat', sigma_slice)





    
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

#    print "Writing E_file for checking"
#
#    print n_k, n_w
#    print sigma[n_w-1][n_k-1][n_k-1]


    greal_file=open("PARSED_Greal_1", "w+")
    gimag_file=open("PARSED_Gimag_1", "w+")
    sigma_file=open("PARSED_SIGMA_1", "w+")
    for w in range (n_w/2, n_w):
#      print w
#      print np.real(g_w[w][0][0])
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
      gimag_file.write(write_string2+"\n")
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
