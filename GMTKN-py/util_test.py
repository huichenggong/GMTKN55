from util import *
from pathlib import Path

test_path = Path("ORCA_output_test/01_.out")  # Not exist
try:
    o1 = ORCAoutput(test_path)
except IOError:
    print("[INFO] File not exist IOError properly caught")

test_path = [Path("ORCA_output_test/01_B97-3c.out"),
             Path("ORCA_output_test/02_DLPNO-DSD-BLYP.out"),
             Path("ORCA_output_test/05_DLPNO-DSD-BLYP-Expen.out")]

o_list = []
print("[INFO] function check_finish")
for p in test_path:
    o_list.append(ORCAoutput(p))
    print(o_list[-1].check_finish())

print("[INFO] function get_energy, get Single Point Energy")
for orca in o_list:
    print("SP Energy", orca.get_energy())

print("[INFO] Test class Strucutre")
s1 = Structure(0, 1)
try:
    s1.get_energy()
except ValueError:
    print("[INFO] Structure energy not set ValueError properly caught")


# Test Read ref data
print("[INFO] Test class Structure")
sub_set = ['RG18', 'ADIM6', 'S22', 'S66', 'HEAVY28', 'WATER27', 'CARBHB12', 'PNICO23', 'HAL59', 'AHB21', 'CHB6', 'IL16',
           'IDISP', 'ICONF', 'ACONF', 'Amino20x4', 'PCONF21', 'MCONF', 'SCONF', 'UPU23', 'BUT14DIOL']
for s in sub_set:
    B_set = BenchmarkSet('../../non-Co/CHARGE_MULTIPLICITY_%s.txt' % s, s)
    B_set.set_ref("%sref.txt" % s)
    index_list, system_list, stoich_list, ref_E_list = B_set.get_ref()
for i in B_set.get_struct_names():
    B_set[i].set_Elevel_ORCA("B3lyp", test_path[0])
    print(B_set[i]["B3lyp"])
    print(o_list[0].get_energy()*627.509469)
    break
