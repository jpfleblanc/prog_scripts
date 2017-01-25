#include<iostream>
#include<fstream>
#include <boost/program_options.hpp>
#include <alps/gf/gf.hpp>
#include <alps/gf/tail.hpp>

typedef alps::gf::three_index_gf<std::complex<double>, alps::gf::matsubara_mesh<alps::gf::mesh::POSITIVE_NEGATIVE>, alps::gf::index_mesh, alps::gf::index_mesh> df_gf_type;
typedef alps::gf::three_index_gf_with_tail<df_gf_type, alps::gf::two_index_gf<double, alps::gf::index_mesh, alps::gf::index_mesh> > df_gf_with_tail;
typedef alps::gf::two_index_gf<double, alps::gf::index_mesh, alps::gf::index_mesh> df_tail_type;

void read_dmft_hifreq(const std::string &input_dmft_file, df_tail_type &c1, df_tail_type &c2, df_tail_type &c3);
df_gf_with_tail read_dual_fermion_gf(const std::string &input_df_file, int nomega4, int kpts, double beta);
df_gf_with_tail read_gf(const std::string &input_dmft_name, const std::string &input_df_name, int nomega4, int kpts, double beta);  
df_gf_with_tail compute_polarization(df_gf_with_tail gf, int nomega4, int nomega4_bose, int kpts, double beta);
int main(int argc, char **argv){
  //define parameter values
  namespace po = boost::program_options;

  std::string input_df_name, input_dmft_name, output_file_name;
  int kpts, nomega4, nomega4_bose;
  double beta;

  po::options_description desc("Allowed options");
  desc.add_options()
  ("help", "show this help")
  ("input_dmft_file", po::value<std::string>(&input_dmft_name), "Input containing the DMFT Green's function and its high frequency information")
  ("input_df_file", po::value<std::string>(&input_df_name), "Input containg the dual fermion Green's function")
  ("output_file", po::value<std::string>(&output_file_name), "Output file containing the GG bubble")
  ("kpts", po::value<int>(&kpts), "number of K points (in x and y direction)")
  ("nfermi", po::value<int>(&nomega4), "number of fermion frequencies")
  ("nbose", po::value<int>(&nomega4_bose), "number of boson frequencies")
  ("beta", po::value<double>(&beta), "inverse temperature")
  ;
  po::variables_map vm;
  po::store(po::parse_command_line(argc, argv, desc), vm);
  po::notify(vm);

  if (vm.count("help")) {
    std::cout<<desc;
    return 1;
  }
  df_gf_with_tail gf=read_gf(input_dmft_name, input_df_name, nomega4, kpts, beta);  

  df_gf_with_tail P=compute_polarization(gf, nomega4, nomega4_bose, kpts, beta);

  alps::hdf5::archive P_file(output_file_name, 'w');
  P.save(P_file, "/P");
}
void read_dmft_hifreq(const std::string &input_dmft_file, df_tail_type &c1, df_tail_type &c2, df_tail_type &c3){
  alps::hdf5::archive ar(input_dmft_file);
  boost::multi_array<double, 2> c2_vec(boost::extents[1][2]); ar["/G_komega/tail/2"]>>c2_vec; 
  boost::multi_array<double, 2> c3_vec(boost::extents[1][2]); ar["/G_komega/tail/3"]>>c3_vec;

  for(alps::gf::index i(0);i<c1.mesh1().extent();++i){
    for(alps::gf::index j(0); j<c1.mesh2().extent();++j){
      c1(i,j)=1.;
      c2(i,j)=c2_vec[0][0];
      c3(i,j)=c3_vec[0][0];
    }
  }
  std::cout<<"read high frequency: c2: "<<c2<<" c3: "<<c3<<std::endl;
}
df_gf_with_tail read_dual_fermion_gf(const std::string &input_df_file, int nomega4, int kpts, double beta){
  alps::hdf5::archive ar(input_df_file);

  double beta_read; ar["/df/parameters/beta"]>>beta_read; if(std::abs(beta-beta_read)>1.e-10) throw std::invalid_argument("beta in parameters and in gf file do not match.");
  std::cout<<" beta: "<<beta<<" read: "<<beta_read<<" nomega4: "<<nomega4<<std::endl;
  int kpts_read; ar["/df/parameters/kpts"]>>kpts_read; if(kpts != kpts_read) throw std::invalid_argument("kpts in parameters and in gf file do not match.");

  boost::multi_array<std::complex<double>, 3> data; ar["/df/glat/data"]>>data;
  std::cout<<"Dual Fermion lattice Green's function extents: "<<data.shape()[0]<<" "<<data.shape()[1]<<" "<<data.shape()[2]<<std::endl;

  df_gf_with_tail gf(df_gf_type(alps::gf::matsubara_mesh<alps::gf::mesh::POSITIVE_NEGATIVE>(beta, 2*nomega4), alps::gf::index_mesh(kpts), alps::gf::index_mesh(kpts), data));
  std::ofstream gf_file("df_glat.dat"); gf_file<<gf;
  return gf;
}
df_gf_with_tail read_gf(const std::string &input_dmft_name, const std::string &input_df_name, int nomega4, int kpts, double beta){
  alps::gf::index_mesh im(kpts);
  df_tail_type c1(im,im);
  df_tail_type c2(im,im);
  df_tail_type c3(im,im);
  read_dmft_hifreq(input_dmft_name, c1, c2, c3);

  df_gf_with_tail gf=read_dual_fermion_gf(input_df_name, nomega4, kpts, beta);
  gf.set_tail(1,c1);
  gf.set_tail(2,c2);
  gf.set_tail(3,c3);

  return gf; 
}
#define f_index(i) matsubara_pn_index(i+n_omega4)
#define b_index(i) matsubara_pn_index(i+n_omega4_bose-1)
#define k_index(i) index_mesh::index_type(i)
df_gf_with_tail compute_polarization_nohifreq(df_gf_with_tail gf, int n_omega4, int n_omega4_bose, int kpts, double beta){
  using namespace alps::gf;
  df_gf_with_tail P(df_gf_type(matsubara_mesh<mesh::POSITIVE_NEGATIVE>(beta, 2*n_omega4_bose-1,statistics::BOSONIC), index_mesh(kpts), index_mesh(kpts)));
  P.initialize();
  //Omega and q are the energy and momentum of P
  for(int Omega=-n_omega4_bose+1;Omega<n_omega4_bose;++Omega){
    for(int qx=0;qx<kpts;++qx){
      for(int qy=0;qy<kpts;++qy){
        //omega and k are the energy and momentum we sum over
        for(int kx=0;kx<kpts;++kx){
          for(int ky=0;ky<kpts;++ky){
            int kx_plus_qx=(kx+qx)%kpts;
            int ky_plus_qy=(ky+qy)%kpts;
            for(int omega=-n_omega4-n_omega4_bose;omega<n_omega4+n_omega4_bose;++omega){
              if(omega+Omega < -n_omega4 || omega+Omega >= n_omega4) continue;
              if(omega       < -n_omega4 || omega       >= n_omega4) continue;
              //dimension of polarization is inverse energy (same as beta)
              P(b_index(Omega),k_index(qx), k_index(qy))-=gf(f_index(omega+Omega), k_index(kx_plus_qx), k_index(ky_plus_qy))*gf(f_index(omega), k_index(kx),k_index(ky))/(beta*kpts*kpts);
            }
          }
        }
      }
    }
  }

  alps::gf::index_mesh im(kpts);
  df_tail_type c1(im,im); c1.initialize(); //no 1/omega term
  P.set_tail(1, c1);
  return P;
}
inline std::complex<double> hifreq(const df_gf_with_tail &gf, int freq, int kx, int ky, double beta){
  using namespace alps::gf;
  std::complex<double> iomegan(0., (2*freq+1)*M_PI/beta);
  return 1./iomegan+gf.tail(2)(k_index(kx),k_index(ky))/(iomegan*iomegan)+gf.tail(3)(k_index(kx),k_index(ky))/(iomegan*iomegan*iomegan);
}
inline std::complex<double> value_minus_hifreq(const df_gf_with_tail &gf, int freq, int kx, int ky, int n_omega4, double beta){
  using namespace alps::gf;
  std::complex<double> iomegan(0., (2*freq+1)*M_PI/beta);
  return gf(f_index(freq), k_index(kx), k_index(ky))-hifreq(gf, freq, kx, ky, beta);
}
df_gf_with_tail compute_polarization(df_gf_with_tail gf, int n_omega4, int n_omega4_bose, int kpts, double beta){
  using namespace alps::gf;
  df_gf_with_tail P(df_gf_type(matsubara_mesh<mesh::POSITIVE_NEGATIVE>(beta, 2*n_omega4_bose-1,statistics::BOSONIC), index_mesh(kpts), index_mesh(kpts)));
  P.initialize();
  //Omega and q are the energy and momentum of P
  for(int Omega=-n_omega4_bose+1;Omega<n_omega4_bose;++Omega){
    for(int qx=0;qx<kpts;++qx){
      for(int qy=0;qy<kpts;++qy){
        //omega and k are the energy and momentum we sum over
        for(int kx=0;kx<kpts;++kx){
          for(int ky=0;ky<kpts;++ky){
            int kx_plus_qx=(kx+qx)%kpts;
            int ky_plus_qy=(ky+qy)%kpts;
            //let this loop run wherever BOTH GF have data
            for(int omega=-n_omega4-n_omega4_bose;omega<n_omega4+n_omega4_bose;++omega){
              if(omega < -n_omega4 || omega >= n_omega4) continue;
              if(omega+Omega < -n_omega4 || omega+Omega >= n_omega4) continue;
              P(b_index(Omega),k_index(qx),k_index(qy))-=value_minus_hifreq(gf, omega+Omega, kx_plus_qx, ky_plus_qy,n_omega4,beta)
                  *value_minus_hifreq(gf, omega, kx,ky, n_omega4, beta)/(beta*kpts*kpts);
            }
            //let this loop run wherever g0(omega) has data
            for(int omega=-n_omega4;omega<n_omega4;++omega){
              P(b_index(Omega),k_index(qx), k_index(qy))-=hifreq(gf, omega+Omega, kx_plus_qx, ky_plus_qy, beta)
                      *value_minus_hifreq(gf, omega, kx,ky, n_omega4, beta)/(beta*kpts*kpts);
            }
            //let this loop run wherever g0(omega+Omega) has data
            for(int omega=-n_omega4-Omega;omega<n_omega4-Omega;++omega){
              P(b_index(Omega),k_index(qx), k_index(qy))-=value_minus_hifreq(gf, omega+Omega, kx_plus_qx, ky_plus_qy, n_omega4,beta)
                      *hifreq(gf, omega, kx, ky, beta)/(beta*kpts*kpts);
            }
          }
        }

        //now add the hifreq sum. Get it from mathematica, using:
        //FullSimplify[Sum[ghf[n] ghf[n + W], {n, -Infinity, Infinity}],
        //Assumptions -> Element[W, Integers]]
        //A couple of constants:
        double pisq=M_PI*M_PI; double pi4=pisq*pisq;
        double betasq=beta*beta; double beta4=betasq*betasq; double beta6=betasq*beta4;
        double Omegasq=Omega*Omega; double Omega4=Omegasq*Omegasq;
        double c2=gf.tail(2)(k_index(0),k_index(0)); double c3=gf.tail(3)(k_index(0),k_index(0));
        //(4 (c2^2 - c3) \[Pi]^2 W^2 \[Beta]^4 +  3 c3^2 \[Beta]^6)/(32 \[Pi]^4 W^4)
        if(Omega!=0){
          P(b_index(Omega),k_index(qx), k_index(qy))-=1./(32*pi4*Omega4)*
              (4.*(c2*c2-c3)*pisq*Omegasq*beta4+3*c3*c3*beta6)/beta;
        }else{
          //1/480 (-120 \[Beta]^2 + 10 (c2^2 + 2 c3) \[Beta]^4 - c3^2 \[Beta]^6)
          P(b_index(Omega),k_index(qx),k_index(qy))-=-beta/4.+(1./48*(c2*c2+2.*c3)*beta4-1./480*c3*c3*beta6)/beta;
        }

      }
    }
  }
  /*for(int Omega=-n_omega4_bose+1;Omega<n_omega4_bose;++Omega){
    for(int qx=0;qx<kpts;++qx){
      for(int qy=0;qy<kpts;++qy){
        //omega and k are the energy and momentum we sum over
        for(int kx=0;kx<kpts;++kx){
          for(int ky=0;ky<kpts;++ky){
            int kx_plus_qx=(kx+qx)%kpts;
            int ky_plus_qy=(ky+qy)%kpts;
            for(int omega=-n_omega4-n_omega4_bose;omega<n_omega4+n_omega4_bose;++omega){
              if(omega+Omega < -n_omega4 || omega+Omega >= n_omega4) continue;
              if(omega       < -n_omega4 || omega       >= n_omega4) continue;
              //dimension of polarization is inverse energy (same as beta)
              P(b_index(Omega),k_index(qx), k_index(qy))-=hifreq(gf, (omega+Omega), (kx_plus_qx), (ky_plus_qy), beta)*hifreq(gf, (omega), (kx),(ky), beta)/(beta*kpts*kpts);
            }
          }
        }
      }
    }
  }*/

  alps::gf::index_mesh im(kpts);
  return P;
}
