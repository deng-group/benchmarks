#!/bin/bash
module add vasp

export machine_config="genoa_64cores"
for i in `find . -mindepth 1 -maxdepth 1 -type d ! -name 'outcars' -exec basename {} \;`
do
        cd $i
        echo $PWD
        mpirun -n 64 vasp_std > vasp.out
        cp OUTCAR ../outcars/${i}.${machine_config}
        cd ..
done
