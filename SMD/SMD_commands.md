Select topology
```bash
gmx pdb2gmx -f REC.pdb -ignh
```

Copy content from 3rd line of lig.gro to the conf.gro file up to the 2nd last line. Check the column number from where the lig.gro data ends (x) in conf.gro and replace the value in 2nd line by x-3. Open file in chimera to check ligand and receptor.
```bash
gmx editconf -f LIG.pdb -o LIG.gro
gedit conf.gro LIG.gro
```
Now, in topol.top file add the ligand itp file and add the ligand molecule number at the bottom

```bash
; Include ligand topology 
#include "LIG.itp"
```

```bash
gmx editconf -f conf.gro -o box.gro -box 10 -bt dodecahedron
gmx solvate -cp box.gro -cs spc216.gro -p topol.top -o box_sol.gro

gmx grompp -f ions.mdp -c box_sol.gro -p topol.top -o ion.tpr   
gmx genion -s ion.tpr -p topol.top -conc 0.1 -neutral -o box_sol_ion.gro

gmx grompp -f em.mdp -c box_sol_ion.gro -p topol.top -o em.tpr
gmx mdrun -v -deffnm em
```
*Make index files for lig posres*
```bash
gmx make_ndx -f LIG.gro -o index_LIG.ndx
```
```bash
gmx genrestr -f LIG.gro -n index_LIG.ndx -o posre_LIG.itp -fc 1000 1000 1000
```

*Open topol.top file and at the end of the document add this*
```bash
		; Ligand position restraints
		#ifdef POSRES
		#include "posre_LIG.itp"
		#endif
```

*Now make a complex in index*

```bash
gmx make_ndx -f em.gro -o index.ndx
```

```bash
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -n index.ndx -o nvt.tpr
gmx mdrun -deffnm nvt -v

gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -p topol.top -n index.ndx -o npt.tpr
gmx mdrun -deffnm NPT -v

gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o md.tpr
gmx mdrun -deffnm md -v

gmx grompp -f smd.mdp -c npt.gro -t md.cpt -p topol.top -r md.gro -n index.ndx -o smd.tpr
gmx mdrun -deffnm smd -v
```

*Post Analysis*
```bash
gmx trjconv -s smd.tpr -f smd.xtc -o smd_center.xtc -center -pbc mol -ur compact
gmx trjconv -s smd.tpr -f smd_center.xtc -n index.ndx -o frame.pdb -dump 1000
```
*H-bonds analyss*
```bash
gmx hbond -f smd_center.xtc -s smd.tpr -n index_res_lig.ndx -num hbonds.xvg
```

*IE For total*
```bash
gmx grompp -f md_IE_total.mdp -c MD.gro -t MD.cpt -p topol.top -r MD.gro -n index.ndx -o md_IE_total.tpr
gmx mdrun -deffnm md_IE_total -rerun smd_center.xtc -nb cpu
gmx energy -f md_IE_total.edr -o IE_total.xvg
```

## Restart run
```bash
gmx mdrun -s smd.tpr -cpi smd.cpt -deffnm smd -pf smd_pullf.xvg -px smd_pullx.xvg -append -v
```
