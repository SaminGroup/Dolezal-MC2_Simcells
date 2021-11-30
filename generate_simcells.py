import ase.io.vasp
import numpy as np
from random import uniform
import simcell_funcs as fun
from scipy.sparse.linalg import gmres



structures = {
'sc'  : 1,
'bcc' : 2,
'fcc' : 4,
'hcp' : 4
}

dims32 = {
'sc'  : [2,4,4],
'bcc' : [2,2,4],
'fcc' : [2,2,2],
'hcp' : [2,2,2]
}

dims48 = {
'sc'  : [3,4,4],
'bcc' : [2,3,4],
'fcc' : [2,2,3],
'hcp' : [2,2,3]
}

def poscar(dims,lattice, Ncells, typecount, names, opsys, genpot):
    dir="base-structures/"
    for i in range(Ncells):
        if lattice[i] == "simple cubic":
            cell = ase.io.vasp.read_vasp(dir+"POSCAR_simple_cubic")
        else:
            cell = ase.io.vasp.read_vasp(dir+"POSCAR_{}".format(lattice[i]))
        ase.io.vasp.write_vasp("POSCAR{}".format(i+1),
                               cell*(int(dims[i][0]),int(dims[i][1]),int(dims[i][2])),
                               label = 'Cell {}'.format(i+1),direct=True,sort=True)

        with open('POSCAR{}'.format(i+1)) as f:
            lines = f.readlines()

        if genpot:
            fun.potcar(names,opsys)
        lines[5] = (' '.join(names)+'\n')
        lines[6] = fun.formatter(typecount[i])
        with open('POSCAR{}'.format(i+1), 'w') as f:
            f.writelines(lines)


print("\n --------------------- User Inputs ---------------------")
opsys = input(" 1. Op. System (windows, linux, unix)? ")
names = input(" 2. Species Names (Au Pt Zr Ti etc)? ").split()
m = len(names)

C = np.asarray(input(" 3. Total system concentration? ").split(),dtype=float)
choice = input(" 4. Do you wish to create your own simcells or use default (y or d)? ")

if choice == 'd':
    N = int(input(" 5. How many atoms total per sim cell (32 or 48)? "))
    cells = ['bcc','fcc','hcp']
    lattice = []
    for i in range(m):
        r = int(uniform(0,3))
        lattice.append(cells[r])

else:
    N = int(input(" 5. How many atoms total per sim cell? "))
    lattice = input(" 5a. Lattice type for each cell (sc bcc fcc hcp) ").split()

A = C*np.ones((m,m))
b = C*N*np.ones(m,)
x = gmres(A.T,b)[0]
x = np.array([int(j) for j in x])

typecount = []
for i in range(m):
    typecount.append([])
    for j in range(m):
        typecount[i].append(int(x[j]))
    if sum(typecount[i]) != N:
        add = N-sum(x)
        select = int(uniform(0,m))
        typecount[i][select] += add


if choice == 'd':
    if N == 32:
        pick = dims32
    else:
        pick = dims48

    dims = np.zeros((m,3))
    for i in range(m):
        dims[i] = pick[lattice[i]]

else:
    dims = np.zeros((m,3))
    for i in range(m):
        val = input(" 5b. Input cell dimensions for Cell {}, {}, which has {} atoms in the unit cell (x y z): ".format(i+1,lattice[i],structures[lattice[i]]))
        val = np.asarray(val.split(),dtype=int)
        dims[i] = val
genpot = input(" 6. Generate POTCARs (y or n)? ")

if genpot == "y" or genpot == "yes":
    genpot = True
else:
    genpot = False

print(" --------------------- procedure initialized ---------------------")

poscar(dims,lattice,m,typecount,names,opsys,genpot)

for i in range(m):
    if genpot:
        print(" ---- Generated POSCAR{} and POTCAR{}".format(i+1,i+1))
    else:
        print(" ---- Generated POSCAR{}".format(i+1))
print(" ----------------------- procedure complete -----------------------")
