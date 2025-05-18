from fresh_core.fresh_core import fuel
import openmc.deplete
from scipy import constants

results = openmc.deplete.Results(filename='depletion_results_before_plates.h5')

# if you add more isotopes, their concentration in the fuel will be outputted in units at%
selected_nuclides = [
    "U232", "U233", "U234", "U235", "U236", "U237", "U238",
    "Pa231", "Th232", "Th231", "Ac227", "Np237", "Pu238",
    "Pu239", "Pu240", "Pu241", "Pu242", "Am241", "Sm149",
    "Tc99", "I129", "Cs135", "Zr93", "Se79", "Ru106",
    "Pd107", "Si28", "Si29", "Si30", "Al27", "C12", "C13",
    "Fe54", "Fe56", "Fe57", "Fe58", "O16", "O17", "O18",
    "N14", "N15"]

nuclides_i_dict = {}
nuclides_f_dict = {}

for nuc in selected_nuclides:
    nuclides_f_dict[nuc] = results.get_atoms(mat=fuel, nuc=nuc, nuc_units='atom/cm3')[1][-1]

for nuc in selected_nuclides:
    nuclides_i_dict[nuc] = results.get_atoms(mat=fuel, nuc=nuc, nuc_units='atom/cm3')[1][0]

total_i = sum(nuclides_i_dict.values())
total_f = sum(nuclides_f_dict.values())

for nuc in nuclides_i_dict:
    nuclides_i_dict[nuc] /= total_i

for nuc in nuclides_f_dict:
    nuclides_f_dict[nuc] /= total_f


uranium_i_total = (nuclides_i_dict["U232"] + nuclides_i_dict["U233"] + nuclides_i_dict["U234"] + nuclides_i_dict["U235"]
                 + nuclides_i_dict["U236"] + nuclides_i_dict["U237"] + nuclides_i_dict["U238"])

uranium_f_total = (nuclides_f_dict["U232"] + nuclides_f_dict["U233"] + nuclides_f_dict["U234"] + nuclides_f_dict["U235"]
                 + nuclides_f_dict["U236"] + nuclides_f_dict["U237"] + nuclides_f_dict["U238"])

u235_fraction_i = nuclides_i_dict["U235"] / uranium_i_total

u235_fraction_f = nuclides_f_dict["U235"] / uranium_f_total


for key, value in nuclides_f_dict.items():
    print(f'{key} = {value} at%')

print(f'\nInitial U235 enrichment: {u235_fraction_i * 100:.2f} at%\nCurrent U235 enrichment: {u235_fraction_f * 100:.2f} at%')

u235_weight_0 = ((results.get_atoms(mat=fuel, nuc='U235', nuc_units='atoms')[1][0]) * 235.043928) / (constants.Avogadro)
u235_weight_1 = ((results.get_atoms(mat=fuel, nuc='U235', nuc_units='atoms')[1][-1]) * 235.043928) / (constants.Avogadro)
pu239_weight_0 = ((results.get_atoms(mat=fuel, nuc='Pu239', nuc_units='atoms')[1][0]) * 239.052162) / (constants.Avogadro)
pu239_weight_1 = ((results.get_atoms(mat=fuel, nuc='Pu239', nuc_units='atoms')[1][-1]) * 239.052162) / (constants.Avogadro)

print(f'\nCurrent Pu239 buildup by weight is {pu239_weight_1 - pu239_weight_0:.6} grams')
print(f'\nCurrent U235 loss by weight is {u235_weight_0 - u235_weight_1:.6} grams')