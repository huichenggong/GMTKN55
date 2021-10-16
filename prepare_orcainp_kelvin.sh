base=$PWD
orca_inp=08_BLYP_SVP_gcp


for subset in ADIM6 AHB21 Amino20x4 BUT14DIOL CARBHB12 CHB6 HAL59 HEAVY28 ICONF IDISP IL16 MCONF PCONF21 PNICO23 RG18 S22 S66 SCONF UPU23 WATER27 
#for subset in ACONF
do
    cd $base/non-Co/$subset
    for s in ./*/
    do
        cd $s
        pwd
        cp $base/ORCA_tmp/$orca_inp.inp ./
        cat orca_charge_mult.txt >> $orca_inp.inp

        echo """#!/bin/bash
#SBATCH --job-name=$subset-$s-$orca_inp
#SBATCH --ntasks-per-node=4
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=3G
#SBATCH --time=0:15:00
#SBATCH --partition=avx512,hipri,k2-hipri
#SBATCH --exclude=node009

echo \$SLURM_JOB_NODELIST
source /mnt/scratch/chemistry-apps/cheng/set_ORCA5.0.1.sh

which orca

/mnt/scratch/chemistry-apps/cheng/orca_5_0_1_linux_x86-64_shared_openmpi411/orca $orca_inp.inp > $orca_inp.out

""" > Run_$orca_inp.sh
        sbatch Run_$orca_inp.sh
        cd ../
    done
done

