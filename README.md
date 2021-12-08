## Dolezal MC2 Simulation Cell Routine

**Please make sure you have Atomic Simulation Environment (ASE) installed before trying to use this tool "pip install ase", "conda install -c conda-forge ase", https://github.com/rosswhitfield/ase

Before calling "generate_simcells.py" make sure you have the right POTCAR files in the potcars/ directory and they are of the form {}_POTCAR (Au_POTCAR, Pt_POTCAR, etc)

The POSCAR1 file in potcars/ can be deleted. Once ready, call generate_simcells.py, "python generate_simcells.py" where a few prompts will appear,

![image](https://user-images.githubusercontent.com/47109396/145228007-ec0dadde-1193-4d29-a81b-a7a3c67581c3.png)

Make sure to list the concentrations in the same order as the line right above it. In both examples I selected "n" for the POTCARs -- only do this if you already have generated all the concatentated POTCARs. Otherwise, select "y", and POTCAR1,...POTCARm will be generated.
