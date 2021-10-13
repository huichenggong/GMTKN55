#####################################
#
#Run this script first to download the structure in GMTKN55 from www.thch.uni-bonn.de
#
#####################################
for name in RG18 ADIM6 S22 S66 HEAVY28 WATER27 CARBHB12 PNICO23 HAL59 AHB21 CHB6 IL16 \
            IDISP ICONF ACONF Amino20x4 PCONF21 MCONF SCONF UPU23 BUT14DIOL
do
    wget www.thch.uni-bonn.de/tc.old/downloads/GMTKN/GMTKN55/$name.tar
    tar xvf $name.tar
    wget www.thch.uni-bonn.de/tc.old/downloads/GMTKN/GMTKN55/CHARGE_MULTIPLICITY_$name.txt
done

