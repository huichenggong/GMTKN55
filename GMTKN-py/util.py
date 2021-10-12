import os
import re

class ORCAoutput:
    def __init__(self, file_name):
        if os.path.isfile(file_name):
            self.file_name=file_name
        else:
            raise IOError("ORCA output file doesn't exist")
        with open(self.file_name) as f:
            self.lines = f.read()
    def check_finish(self):
        if "ORCA TERMINATED NORMALLY" in self.lines:
            return True
        else:
            return False

    def get_energy(self, unit="Hartree"):
        """Single Point Energy in Hartree"""
        p = re.search(r'FINAL SINGLE POINT ENERGY.*', self.lines)
        if not p: # if re doesn't match, p is None, raise Error
            raise IOError('Can not find"FINAL SINGLE POINT ENERGY"')
        else:
            E = float(p.group(0).split()[-1])
            if unit=="Hartree":
                return E
            if unit=="kcal/mol":
                return E * 627.509469
            else:
                raise ValueError("Energy Unit Can not understand")

class Structure:
    def __init__(self, charge, multiplicity):
        """
        :param charge: int
        :param multiplicity: int
        """
        if isinstance(charge, int) and isinstance(multiplicity, int):
           pass
        else:
            raise ValueError("Charge and Multiplicity should be int")
        self.charge = charge
        self.multiplicity = multiplicity
        self.energy = {}

    def __str__(self):
        return str(self.energy)

    def __repr__(self):
        return str(self.energy)

    def __getitem__(self, level):
        if not level in self.energy:
            raise ValueError("Calculation level not found in this structure")
        else:
            return self.energy[level]

    def set_Elevel(self, level, energy):
        self.energy[level] = energy

    def get_Elevel(self, level):
        return self[level]

    def set_Elevel_ORCA(self, level, file_name):
        o_out = ORCAoutput(file_name)
        self.energy[level] = o_out.get_energy(unit="kcal/mol")

    def get_energy(self):
        """get the whole energy dictionary"""
        if not self.energy:
            raise ValueError("Energy haven't been set")
        else:
            return self.energy

    def get_charge(self):
        return self.charge

    def get_multiplicity(self):
        return self.multiplicity


class BenchmarkSet:
    def __init__(self, file_name, set_name):
        self.set_name = set_name
        #Check file existence
        if os.path.isfile(file_name):
            pass
        else:
            raise IOError("Charge-Multilicity file doesn't exist")
        #Build structure inf table
        self.struct_table = {}
        with open(file_name) as f:
            lines = f.readlines()
        for line in lines:
            #print(line)
            struc_name, charge, mul = line.split()
            self.struct_table[struc_name] = Structure(int(charge), int(mul))

        self.index_list = []
        self.ref_E_list = []
        self.system_list = []
        self.stoich_list = []

    def __str__(self):
        return str(self.set_name)+':'+str(list(self.struct_table.keys()))

    def __repr__(self):
        return "BenchmarkSet<"+str(self.set_name)+':'+str(list(self.struct_table.keys()))+'>'

    def __getitem__(self, struct):
        return self.struct_table[struct]

    def get_set_name(self):
        return self.set_name

    def get_struct_names(self):
        return self.struct_table.keys()

    def set_ref(self, file_name):
        # Check file existence
        if os.path.isfile(file_name):
            pass
        else:
            raise IOError("Ref file doesn't exist")
        with open(file_name) as f:
            ref_lines = f.readlines()

        self.index_list = []
        self.ref_E_list = []
        self.system_list = []
        self.stoich_list = []
        self.bench_data = {}

        for i in ref_lines[5:]:
            data_raw = i.split()
            if len(data_raw) < 6:
                break
            index = int(data_raw[0])
            ref_E = float(data_raw[-1])
            if len(data_raw) % 2 == 1:
                raise ValueError("Systems with Stoichiometry number in total should be even")
            else:
                self.index_list.append(index)
                self.ref_E_list.append(ref_E)
                system = data_raw[1:len(data_raw) // 2]
                self.system_list.append(system)
                stoich = [float(i) for i in data_raw[len(data_raw) // 2:-1]]
                self.stoich_list.append(stoich)
        return self.index_list, self.system_list, self.stoich_list, self.ref_E_list

    def get_ref(self):
        """
        :return: index, system, stoich, reference_Energy
        """
        if self.index_list:
            return self.index_list, self.system_list, self.stoich_list, self.ref_E_list
        else:
            raise ValueError("Ref haven't been set")

    def get_ref_num(self):
        if self.index_list:
            return len(self.index_list)
        else:
            raise ValueError("Ref haven't been set")

    def calc_benchmark_data(self, level):
        if level in self.bench_data.keys():
            raise ValueError("The same level has been calculated")
        else:
            self.bench_data[level] = []
        for system, stoich in zip(self.system_list, self.stoich_list):
            if len(system) != len(stoich):
                raise ValueError("Number of system and number of stoich should be the same!")
            energy = 0
            for item, num in zip(system, stoich):
                energy += self[item][level] * num
            self.bench_data[level].append(energy)

    def get_benchmark_data(self, level):
        if not level in self.bench_data.keys():
            raise ValueError("This level of benchmark hasn't been calculated")
        else:
            return self.bench_data[level]
