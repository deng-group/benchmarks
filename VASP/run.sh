#!/bin/bash -l

module load VASP/6.4.1-gnu-9654

machine_config="genoa_96cores_9654_single"
mpinp=96
for i in `find . -mindepth 1 -maxdepth 1 -type d ! -name 'outcars' -exec basename {} \;`
do
        cd $i
        echo $PWD
        mpirun -n $mpinp vasp_std > vasp.out
        cp OUTCAR ../outcars/${i}.${machine_config}
        gzip ../outcars/${i}.${machine_config}
        cd ..
done
