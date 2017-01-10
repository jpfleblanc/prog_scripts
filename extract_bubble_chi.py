# An example of parsing df data
import h5py
import numpy as np
from numpy import pi
import re

from scipy import special

	



def main(fname = "bubble.h5", verbosity = 1):

    h5file = h5py.File("output.h5", "r")
    data = h5file["df"]
    # import lattice gf
    (grids, glat) = read_hdf5(data["glat"])
    # extract grid of Matsubara values (it is stored as a complex number, so h5py imports into 
    wgrid = grids[0].copy()[:,1]
    # extract grid of k-points (in one of the dimensions)
    kgrid = grids[1].copy()


    h5file = h5py.File(fname, "r")
    data = h5file
    # import lattice gf
    P = np.array(h5file["P/data"])
    nbose=np.array(h5file["P/mesh/1/N"])
    nkpts=np.array(h5file["P/mesh/2/N"])

    print P
    print nbose

    bubble_collect=[]

    for bose in range (0, nbose):
        for kpts1 in range (0, nkpts):
            for kpts2 in range (0, nkpts):
                print kgrid[kpts1], kgrid[kpts2], bose, P[bose][kpts1][kpts2]
                bubble_collect.append((kgrid[kpts1], kgrid[kpts2], bose-nbose/2, P[bose][kpts1][kpts2][0],P[bose][kpts1][kpts2][1]))

    print bubble_collect


    np.savetxt("bubble.dat", bubble_collect)

    print "Correcting chi_file.dat"
    qx, qy, w, real_chi, im_chi= np.loadtxt("chi_file.dat", unpack=True)

    chi_corrected_dataset=[]
    for i in range(0,len(real_chi)):
      chi_corrected_dataset.append((qx[i], qy[i],w[i], real_chi[i]+0.5*bubble_collect[i][3], im_chi[i]+0.5*bubble_collect[i][4]))

	

    np.savetxt('chi_corrected.dat', chi_corrected_dataset)



def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    '''    
    return [ str(c) for c in re.split('([-]?\d+)', text) ]

    
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
