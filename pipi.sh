awk '$1==3.141592653589793116 && $2==$1 && $3==0 {print $3,$4,$5}' chi_extrapolated.dat
