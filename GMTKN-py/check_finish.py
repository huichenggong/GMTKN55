from pathlib import Path
import sys
import os

sub_set = ['RG18', 'ADIM6', 'S22', 'S66', 'HEAVY28', 'WATER27', 'CARBHB12', 'PNICO23', 'HAL59', 'AHB21', 'CHB6', 'IL16',
           'IDISP', 'ICONF', 'ACONF', 'Amino20x4', 'PCONF21', 'MCONF', 'SCONF', 'UPU23', 'BUT14DIOL']
base = Path(os.getcwd())
base = base.parent / "non-Co"

def check_orca_finish(orca_file):
    """
    Check the second final line in orca out put
    if "ORCA TERMINATED NORMALLY" present True
    """
    if not os.path.isfile(orca_file):
        return False
    with open(orca_file) as f:
        orca_out = f.readlines()
        if len(orca_out) <=3:
            return False
        if "ORCA TERMINATED NORMALLY" in orca_out[-2]:
            return True
        else:
            return False


###Check finish
f_name = "06_DSD-BLYP"
rerun_ls = []
for s in sub_set:
    char_mul = base/("CHARGE_MULTIPLICITY_%s.txt"%s)
    f1 = base/s
    print("#",s)
    with open(char_mul, 'r') as f:
        lines = f.readlines()
    for line in lines:
        struc_name, charge, mul = line.split()
        struc_fold = f1/struc_name
        orca_file = struc_fold/(f_name+".out")
        if not check_orca_finish(orca_file):
            print("cd",struc_fold)
            print("sbatch K-06.sh")

