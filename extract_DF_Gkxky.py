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

#    (grids, sigma_lat_pz) = read_hdf5(data["fluct_diag/sigma_lat_3.14159_0"])
#    (grids, sigma_lat_p2p2) = read_hdf5(data["fluct_diag/sigma_lat_1.5708_1.5708"])
#    bose_grid= grids[0].copy()[:,1]
 #   fermi_grid= grids[1].copy()[:,1]
  #  qx_grid= grids[2].copy()
   # qy_grid= grids[3].copy()

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

# printing full G in kx and ky
    kx_grid=kgrid
    ky_grid=kgrid
    kstep=2.0*np.pi/len(kx_grid)

    g_collect=[]
    df_gg=np.zeros(len(wgrid), dtype=complex)
  
    for om in range(0, len(wgrid)):
      for i in range(0,len(kx_grid)):
        for j in range(0, len(ky_grid)):
        
        #  print om, i, j
#           g_collect.append((kx_grid[i],ky_grid[j], (om - len(wgrid)/2+0.5), np.real(g[om][i][j])[0], np.imag(g[om][i][j])[0]))
         # g_collect.append((kx_grid[i],ky_grid[j], wgrid[om], np.real(g[om][i][j])[0], np.imag(g[om][i][j])[0]))
           g_collect.append((kx_grid[i],ky_grid[j], int(om - len(wgrid)/2), np.real(g[om][i][j])[0], np.imag(g[om][i][j])[0]))
           #print g[om][i][j][0]
           df_gg[om]+=-g[om][i][j][0]*g[om][i][j][0]*kstep*kstep/np.pi/np.pi#/beta/beta

    gg_collect=[]
    for om in range(0, len(wgrid)):
      gg_collect.append((int(om - len(wgrid)/2),np.real(df_gg[om]), np.imag(df_gg[om])))


    np.savetxt("gkxky_file.dat", g_collect)
    np.savetxt("df_gg.dat", gg_collect)



#############
    sigma_collect=[]
    ganti=[]
    kxwanted=0.0
    kywanted=3.14159
    for kx in range (n_kpoints):
      for ky in range (n_kpoints):
        for w in range(n_wpoints/2, n_wpoints):
          if abs(kxwanted-kgrid[kx])<0.001 and abs(kywanted-kgrid[ky])<0.001:
        #    print kx, ky, kgrid[kx], kgrid[ky]
	    sigma_collect.append((2*np.pi/beta*(w-n_wpoints/2+0.5), kgrid[kx], kgrid[ky], np.real(sigma[w][kx][ky])[0], np.imag(sigma[w][kx][ky])[0]))
	    ganti.append((2*np.pi/beta*(w-n_wpoints/2+0.5), kgrid[kx], kgrid[ky], np.real(g[w][kx][ky])[0], np.imag(g[w][kx][ky])[0]))

    np.savetxt("sigma_output_antinodal.dat", sigma_collect)
    np.savetxt("g_output_antinodal.dat", ganti)

    sigma_collect=[]
    gnode=[]
    kxwanted=3.14159265/2.0
    kywanted=3.14159265/2.0
    for kx in range (n_kpoints):
      for ky in range (n_kpoints):
        for w in range(n_wpoints/2, n_wpoints):
          if abs(kxwanted-kgrid[kx])<0.001 and abs(kywanted-kgrid[ky])<0.001:
	    sigma_collect.append((2*np.pi/beta*(w-n_wpoints/2+0.5), kgrid[kx], kgrid[ky], np.real(sigma[w][kx][ky])[0], np.imag(sigma[w][kx][ky])[0]))
	    gnode.append((2*np.pi/beta*(w-n_wpoints/2+0.5), kgrid[kx], kgrid[ky], np.real(g[w][kx][ky])[0], np.imag(g[w][kx][ky])[0]))

    np.savetxt("sigma_output_nodal.dat", sigma_collect)
    np.savetxt("g_output_nodal.dat", gnode)

#############

# write plottable fluct_diag file
#    diag_collect=[]

#    for qx in range (len(qx_grid)):
#      for qy in range (n_kpoints):
#        diag_collect.append((qx_grid[qx], qy_grid[qy], (sigma_lat_pz[len(bose_grid)/2][len(fermi_grid)/2][qx][qy])[1], (sigma_lat_p2p2[len(bose_grid)/2][len(fermi_grid)/2][qx][qy])[1]))

#    np.savetxt("fluct_diag_node-antinode.dat", diag_collect)

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
