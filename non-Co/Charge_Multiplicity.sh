#####################################
#
#Run download.sh before runing this
#
# This script will write the 
# * xyzfile charge multiplicity struc.xyz
# line in orca input file name as orca_charge_mult.txt in each structure folders
#
# The orca_charge_mult.txt will later be assembled into the full orca input file
#
#####################################
for name in RG18 ADIM6 S22 S66 HEAVY28 WATER27 CARBHB12 PNICO23 HAL59 AHB21 CHB6 IL16 \
            IDISP ICONF ACONF Amino20x4 PCONF21 MCONF SCONF UPU23 BUT14DIOL
do
    echo "##############"
    echo "CHARGE_MULTIPLICITY_$name.txt"
    echo "##############"
    while read p; do
        #echo "$p"
        IFS=' '     # space is set as delimiter
        read -ra ADDR <<< "$p"   # str is read into an array as tokens separated by IFS
        #ls $name/${ADDR[0]}
        echo "* xyzfile" "${ADDR[1]}" "${ADDR[2]}" "struc.xyz" > $name/${ADDR[0]}/orca_charge_mult.txt
    done <CHARGE_MULTIPLICITY_$name.txt
    
    #break
done