#!/bin/bash
machine_config=$1
mpinp=$2

for i in `find . -mindepth 1 -maxdepth 1 -type d ! -name 'outcars' -exec basename {} \;`
do
        cd $i
        echo $PWD
        mpirun -n $mpinp vasp_std > vasp.out
        cp OUTCAR ../outcars/${i}.${machine_config}
        gzip ../outcars/${i}.${machine_config}
        cd ..
done
