mace_md:
	cd MACE && bash run_md.sh $(machine_config)

vasp:
	cd VASP && bash run_vasp.sh $(machine_config) ${nproc}