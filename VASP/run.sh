#!/bin/bash
module add vasp

for i in `ls -d */`
do
	cd $i
	echo $PWD
	nkpt=`grep NKPTS outcar.* | awk '{print $4}'`
	if [ $nkpt -gt 1 ]
	then	
		echo "$nkpt greater than 1, run vasp_std"
		#mpirun -n 1 vasp_std > vasp.out
	else
		echo "$nkpt is equal to 1, run vasp_gam"
		#mpirun -n 1 vasp_gam > vasp.out
	fi
	cd ..
done
