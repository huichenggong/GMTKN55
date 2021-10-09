import urllib.request as ul

import pandas as pd
from bs4 import BeautifulSoup
import re

sub_set = ['RG18', 'ADIM6', 'S22', 'S66', 'HEAVY28', 'WATER27', 'CARBHB12', 'PNICO23', 'HAL59', 'AHB21', 'CHB6', 'IL16',
           'IDISP', 'ICONF', 'ACONF', 'Amino20x4', 'PCONF21', 'MCONF', 'SCONF', 'UPU23', 'BUT14DIOL']
#sub_set = [ 'S66', 'HEAVY28', 'MCONF']


def download_GMTKN(url):
    soup = BeautifulSoup(ul.urlopen(url).read(),'html.parser')
    txt = soup.text
    p = re.search(r'#.*', txt, flags=re.DOTALL)

    index_list = []
    ref_E_list = []
    system_list = []
    stoich_list = []

    if p:
        ref_data_raw = p.group(0)
        #print(ref_data_raw)
        ref_lines = ref_data_raw.split('\n')
        for i in ref_lines[5:]:
            data_raw = i.split()
            if len(data_raw) < 6:
                break
            index = int(data_raw[0])
            ref_E = float(data_raw[-1])
            if len(data_raw) % 2 ==1:
                raise ValueError("Systems with Stoichiometry number in total should be even")
            else:
                index_list.append(index)
                ref_E_list.append(ref_E)

                system = data_raw[1:len(data_raw)//2]
                system_list.append(system)

                stoich = [float(i) for i in data_raw[len(data_raw)//2:-1]]
                stoich_list.append(stoich)
    return index_list, system_list, stoich_list, ref_E_list

def download_GMTKN_to_txt(url,txt_file):
    soup = BeautifulSoup(ul.urlopen(url).read(), 'html.parser')
    txt = soup.text
    p = re.search(r'#.*', txt, flags=re.DOTALL)
    if p:
        ref_data_raw = p.group(0)
    else:
        raise ValueError('Can not find tag "#"')
    ref_data_raw = ref_data_raw.replace('/table>', '')
    ref_data_raw = ref_data_raw.replace('~', '')
    with open(txt_file, 'w') as f:
        f.write(ref_data_raw)



for s in sub_set:
    url = 'http://www.thch.uni-bonn.de/tc.old/downloads/GMTKN/GMTKN55/%sref.html'%(s)
    download_GMTKN_to_txt(url,s+'ref.txt')




