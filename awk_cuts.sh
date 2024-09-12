awk '$1==3.141592653589793116 && $2==0 {print}' realfreq.dat > piz.dat
awk '$1==2.748893571891068976e+00 && $2==0 {print}' realfreq.dat > 7pio8z.dat
awk '$1==2.356194490192344837e+00 && $2==0 {print}' realfreq.dat > 6pio8z.dat
awk '$1==1.963495408493620697e+00 && $2==0 {print}' realfreq.dat > 5pio8z.dat
awk '$1==1.570796326794896558e+00 && $2==0 {print}' realfreq.dat > 4pio8z.dat
awk '$1==1.178097245096172418e+00 && $2==0 {print}' realfreq.dat > 3pio8z.dat
awk '$1==7.853981633974482790e-01 && $2==0 {print}' realfreq.dat > 2pio8z.dat
awk '$1==3.926990816987241395e-01 && $2==0 {print}' realfreq.dat > 1pio8z.dat
awk '$1==0 && $2==0 {print}' realfreq.dat > 0pio8z.dat



awk '$1==3.141592653589793116 && $2==$1 {print}' realfreq.dat > diag_pi.dat
awk '$1==2.748893571891068976e+00 && $2==$1 {print}' realfreq.dat > diag_7pio8.dat
awk '$1==2.356194490192344837e+00 && $2==$1 {print}' realfreq.dat > diag_6pio8.dat
awk '$1==1.963495408493620697e+00 && $2==$1 {print}' realfreq.dat > diag_5pio8.dat
awk '$1==1.570796326794896558e+00 && $2==$1 {print}' realfreq.dat > diag_4pio8.dat
awk '$1==1.178097245096172418e+00 && $2==$1 {print}' realfreq.dat > diag_3pio8.dat
awk '$1==7.853981633974482790e-01 && $2==$1 {print}' realfreq.dat > diag_2pio8.dat
awk '$1==3.926990816987241395e-01 && $2==$1 {print}' realfreq.dat > diag_1pio8.dat
awk '$1==0 && $2==0 {print}' realfreq.dat > diag_0pio8.dat

awk '$2==3.141592653589793116 && $1==3.141592653589793116 {print}' realfreq.dat > pzcut_pipi.dat
awk '$2==2.748893571891068976e+00 && $1==3.141592653589793116 {print}' realfreq.dat > pzcut_7pio8z.dat
awk '$2==2.356194490192344837e+00 && $1==3.141592653589793116 {print}' realfreq.dat > pzcut_6pio8z.dat
awk '$2==1.963495408493620697e+00 && $1==3.141592653589793116 {print}' realfreq.dat > pzcut_5pio8z.dat
awk '$2==1.570796326794896558e+00 && $1==3.141592653589793116 {print}' realfreq.dat > pzcut_4pio8z.dat
awk '$2==1.178097245096172418e+00 && $1==3.141592653589793116 {print}' realfreq.dat > pzcut_3pio8z.dat
awk '$2==7.853981633974482790e-01 && $1==3.141592653589793116 {print}' realfreq.dat > pzcut_2pio8z.dat
awk '$2==3.926990816987241395e-01 && $1==3.141592653589793116{print}' realfreq.dat > pzcut_1pio8z.dat
awk '$2==0 && $1==3.141592653589793116 {print}' realfreq.dat > pzcut_0pio8z.dat
