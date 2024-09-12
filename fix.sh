awk '{print (-$5+9.155271918543055776)*sqrt(2),$3}' slice4.dat > tmp1.dat
awk '{print ($5+2.22144169),$3}' slice1.dat > tmp2.dat
cat tmp1.dat tmp2.dat > tmp.dat


