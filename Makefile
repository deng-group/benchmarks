mace_md:
	cd MACE && bash run_md.sh ${machine_config} ${device}

mace_train:
	cd MACE && bash run_train.sh ${machine_config} ${device}

vasp:
	cd VASP && bash run_vasp.sh ${machine_config} ${nproc}