from ase import units
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution,Stationary
from ase.md.nvtberendsen import NVTBerendsen
# from ase.md.nptberendsen import NPTBerendsen
from ase.md import MDLogger
from mace.calculators import MACECalculator
from time import perf_counter
import os, sys
from ase.io import read
from ase.build.supercells import make_supercell
import numpy as np
import argparse
import urllib.request

def run_md(atoms,calc,output_dir,output_name,seed=1234):
    # Print statements
    def print_dyn():
        imd = dyn.get_number_of_steps()
        etot  = atoms.get_total_energy()
        temp_K = atoms.get_temperature()
        stress = atoms.get_stress(include_ideal_gas=True)/units.GPa
        stress_ave = (stress[0]+stress[1]+stress[2])/3.0
        elapsed_time = perf_counter() - start_time
        print(f"  {imd: >3}   {etot:.3f}    {temp_K:.2f}    {stress_ave:.2f}  {stress[0]:.2f}  {stress[1]:.2f}  {stress[2]:.2f}  {stress[3]:.2f}  {stress[4]:.2f}  {stress[5]:.2f}    {elapsed_time:.3f}")
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        print(f'{output_dir} exists, skip mkdir...')
        pass
    log_filename = f"{output_dir}/{output_name}.log"

    # input parameters
    time_step    = 1.0    # fsec
    temperature  = 800    # Kelvin
    num_md_steps = 1000
    num_interval = 100
    taut         = 1.0    # fs

    atoms.calc = calc

    # Set the momenta corresponding to the given "temperature"
    MaxwellBoltzmannDistribution(atoms, temperature_K=temperature,force_temp=True,rng=np.random.RandomState(seed))
    Stationary(atoms)  # Set zero total momentum to avoid drifting

    dyn = NVTBerendsen(atoms, time_step*units.fs, temperature_K = temperature, taut=taut*units.fs, loginterval=num_interval, trajectory=None)
    dyn.attach(print_dyn, interval=num_interval)
    dyn.attach(MDLogger(dyn, atoms, log_filename, header=True, stress=True, peratom=True, mode="w"), interval=num_interval)

    # run MD
    start_time = perf_counter()
    print(f"    imd     Etot(eV)    T(K)    stress(mean,xx,yy,zz,yz,xz,xy)(GPa)  elapsed_time(sec)")
    dyn.run(num_md_steps)  # take 10000 steps

# Parse command line arguments
parser = argparse.ArgumentParser(description='Run molecular dynamics simulation.')
parser.add_argument('--dtype', type=str, help='Data type for the MACE calculator', default='float64')
parser.add_argument('--seed', type=int, help='Random seed for the simulation', default=1234)
parser.add_argument('--device', type=str, help='Device for the MACE calculator', default='cuda')
args = parser.parse_args()

dtype = args.dtype
seed = args.seed

atoms = read('Na3SbS4_cubic.vasp')
atoms = make_supercell(prim=atoms, P=[[5, 0, 0], [0, 5, 0], [0, 0, 5]])
print(f"Total number of atoms: {atoms.get_number_of_atoms()}")
print(f"dtype = {dtype}")
print(f"Seed = {seed}")

# Try to download the model file if it doesn't exist
file_name = "mace_agnesi_medium.model"
url = "https://github.com/ACEsuit/mace-mp/releases/download/mace_mp_0b/mace_agnesi_medium.model"
if not os.path.exists(file_name):
    print(f"{file_name} does not exist. Downloading...")
    try:
        urllib.request.urlretrieve(url, file_name)
        print(f"{file_name} has been downloaded successfully.")
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")
else:
    print(f"{file_name} already exists.")

calc = MACECalculator(model_paths='mace_agnesi_medium.model', default_dtype=dtype, device='cuda')
run_md(atoms, calc, 'md', f'Na3SbS4_{dtype}_{seed}', seed)
