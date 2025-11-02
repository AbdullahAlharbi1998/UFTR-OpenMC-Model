import openmc
import openmc as mc
import numpy as np
from openmc.lib import tally
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

mc.config['cross_sections'] = "/home/eastdusty/openmc_env/share/data/endfb80/endfb-vii.1-hdf5/cross_sections.xml"
# The cross-sections library used in this model was ENDF/B-VIII.0
# It can be downloaded using this link: https://openmc.org/official-data-libraries/

# /home/eastdusty/openmc_env/share/data/endfb80/endfb-viii.0-hdf5/cross_sections.xml



#####################################################################################
#                              MATERIALS DEFINITION                                 #
#####################################################################################

'''
The below is the total volume of both fuel and cadmium, it was calculated because it is mandatory to be provided in order to run a depletion 
calculation, cadmium of course turned out to have negligible change, the lost fraction of Cd-113 at 105,000 kWh was less than 0.1%
'''

fuel_plate_volume = ((30.01 * 2) * (2.98 * 2) * (0.0255 * 2)) * 14 * 22
fuel_plate_mass = 5.5 * ((30.01 * 2) * (2.98 * 2) * (0.0255 * 2))

cadmium_volume = ((((34.3 + 27.9)/2) * (12.7) * (0.102)) * 3) + (((30.5 + 27.9)/2) * (4.57) * (0.102))
total_impurity_fraction = 9.0677574E-04

fuel = mc.Material(name='U3Si2Al')
fuel.set_density('g/cm3', 5.55)

fuel.volume = fuel_plate_volume
fuel.depletable = True

normalizer = 1.24736357E+01 / 1.250E+01

# Uranium content in U3Si2-Al
fuel.add_nuclide('U234', 1.03E-01 , 'wo')
fuel.add_nuclide('U235', 1.24736357E+01 , 'wo')
fuel.add_nuclide('U236', 6.57E-02 , 'wo')
fuel.add_nuclide('U238', 5.08E+01 , 'wo')

# Silicon in U3Si2-Al
fuel.add_element('Si', 5E+00 , 'wo')

# Aluminum in U3Si2-Al
fuel.add_element('Al', 3.23E+01 , 'wo')


# impurities cited from the Safety Analysis Report which reported the impurities based on BWXT (fuel and cladding manufacturer) estimates
fuel.add_element("Al", (fuel_plate_mass * (8.95E-05)), "wo")
fuel.add_element("Ba", (fuel_plate_mass * (1.36E-06)), "wo")
fuel.add_element("Be", (fuel_plate_mass * (3.40E-07)), "wo")
fuel.add_element("B",  (fuel_plate_mass * ((1.82E-07) + (3.21E-06))), "wo")
fuel.add_element("Cd", (fuel_plate_mass * ((3.40E-07) + (3.21E-06))), "wo")
fuel.add_element("Ca", (fuel_plate_mass * (1.36E-05)), "wo")
fuel.add_element("C",  (fuel_plate_mass * (1.66E-04)), "wo")
fuel.add_element("Cr", (fuel_plate_mass * (1.25E-05)), "wo")
fuel.add_element("Co", (fuel_plate_mass * (3.40E-06)), "wo")
fuel.add_element("Cu", (fuel_plate_mass * ((6.85E-05) + (3.21E-06))), "wo")
fuel.add_element("Eu", (fuel_plate_mass * (1.36E-07)), "wo")
fuel.add_element("Gd", (fuel_plate_mass * (1.36E-07)), "wo")
fuel.add_element("Fe", (fuel_plate_mass * ((4.13E-04) + (5.35E-04))), "wo")
fuel.add_element("Pb", (fuel_plate_mass * (3.3974E-07)), "wo")
fuel.add_element("Li", (fuel_plate_mass * ((6.80E-08) + (3.21E-06))), "wo")
fuel.add_element("Mg", (fuel_plate_mass * (6.80E-06)), "wo")
fuel.add_element("Mn", (fuel_plate_mass * (5.89E-06)), "wo")
fuel.add_element("Mo", (fuel_plate_mass * (2.04E-06)), "wo")
fuel.add_element("Ni", (fuel_plate_mass * (2.94E-05)), "wo")
fuel.add_element("N",  (fuel_plate_mass * (3.74E-05)), "wo")
fuel.add_element("P",  (fuel_plate_mass * (1.36E-05)), "wo")
fuel.add_element("Sm", (fuel_plate_mass * (1.36E-07)), "wo")
fuel.add_element("Ag", (fuel_plate_mass * (6.79E-07)), "wo")
fuel.add_element("Na", (fuel_plate_mass * (6.79E-06)), "wo")
fuel.add_element("Sn", (fuel_plate_mass * (6.79E-07)), "wo")
fuel.add_element("W",  (fuel_plate_mass * (1.47E-05)), "wo")
fuel.add_element("V",  (fuel_plate_mass * (3.06E-06)), "wo")
fuel.add_element("Zn", (fuel_plate_mass * ((1.36E-05) + (6.41E-05))), "wo")
fuel.add_element("Zr", (fuel_plate_mass * (2.60E-06)), "wo")
fuel.add_element("O",  (fuel_plate_mass * 3.11E-04), "wo")



# Cladding
Al6061 = mc.Material(name='Al6061')

# Composition also cited from the Safety Analysis Report which reported the impurities based on BWXT (fuel and cladding manufacturer) estimates
Al6061.add_element("Al", 97.599, "wo")
Al6061.add_element("Si", 0.500, "wo" )
Al6061.add_element("Fe", 0.354, "wo" )
Al6061.add_element("Cu", 0.294, "wo")
Al6061.add_element("Mn", 0.070, "wo" )
Al6061.add_element("Mg", 0.924, "wo" )
Al6061.add_element("Cr", 0.135, "wo" )
Al6061.add_element("Zn", 0.089, "wo" )
Al6061.add_element("V",  0.010, "wo" )
Al6061.add_element("Zr", 0.003, "wo" )
Al6061.add_element("B",  0.001, "wo" )
Al6061.add_element("Co", 0.001, "wo" )
Al6061.add_element("Ga", 0.005, "wo" )
Al6061.add_element("Cd", 0.001, "wo" )
Al6061.add_element("Li", 0.001, "wo")

Al6061.set_density('g/cm3', 2.7)

Al6061.depletable = False



water = mc.Material(name='Water')
water.add_element('H', 2)
water.add_element('O', 1)
water.set_density('g/cm3', 0.996)
water.add_s_alpha_beta('c_H_in_H2O')

water.depletable = False


# 5 ppm boron impurity in graphite is reported in the Safety Analysis Report to be estimated via chemical analysis done on a sample of that nuclear grade graphite at Idaho National Laboratory (INL)
'''
The true density of graphite is 1.6 g/cm3. However, using CSG to define the geometry instead of CAD really overestimates 
the content of graphite, as it fills gaps that are caused by stacking, holes within some graphite blocks for irradiation 
purposes, and other geometric considerations causing less concentration of graphite within the core. Therefore, the density 
of graphite was reduced slightly by 0.005 g/cm3 which produced slightly more consistent results.
'''
graphite = mc.Material(name='graphite')
graphite.add_element('C', 1 - 5e-6)
graphite.add_element('B', 5e-6)
graphite.set_density('g/cm3', 1.595)
graphite.add_s_alpha_beta('c_Graphite')

graphite.depletable = False


cadmium = mc.Material(name='cadmium')
cadmium.add_element('Cd', 1)
cadmium.set_density('g/cm3', 8.75)
# cadmium.volume = cadmium_volume
# cadmium.depletable = True



magnesium = mc.Material(name='magnesium')
magnesium.add_element('Mg', 1)
magnesium.set_density('g/cm3', 1.74)

magnesium.depletable = False



air = mc.Material(name='Air')
air.add_element('O', 0.21)
air.add_element('N', 0.78)
air.add_element('Ar', 0.00995)
air.add_element('C', 0.00005)
air.set_density('g/cm3', 0.0012)

air.depletable = False



barite_concrete = mc.Material(name='barytes_concrete')
barite_concrete.add_element('Ba', 0.481, 'wo')
barite_concrete.add_element('O', 0.324, 'wo')
barite_concrete.add_element('S', 0.114, 'wo')
barite_concrete.add_element('Ca', 0.042, 'wo')
barite_concrete.add_element('Si', 0.01, 'wo')
barite_concrete.add_element('Mg', 0.007, 'wo')
barite_concrete.add_element('C', 0.006, 'wo')
barite_concrete.add_element('Fe', 0.006, 'wo')
barite_concrete.add_element('H', 0.006, 'wo')
barite_concrete.add_element('Al', 0.004, 'wo')
barite_concrete.set_density('g/cm3', 3.5)

barite_concrete.depletable = False



materials = mc.Materials([fuel, Al6061, water, air, graphite, barite_concrete, cadmium, magnesium])


colors = {fuel: 'red', Al6061: 'silver', water: 'blue', graphite: 'grey', air: 'black',
          cadmium: 'green', magnesium: 'purple', barite_concrete: 'saddlebrown'}





#####################################################################################
#                                   FUEL PLATE                                      #
#####################################################################################

FUEL_WIDTH = 5.96

fuel_top = mc.ZPlane(z0=30.01)
fuel_bottom = mc.ZPlane(z0=-30.01)
fuel_right = mc.XPlane(x0=FUEL_WIDTH/2)
fuel_left = mc.XPlane(x0=-FUEL_WIDTH/2)
fuel_front = mc.YPlane(y0=0.0255)
fuel_back = mc.YPlane(y0=-0.0255)

fuel_region = +fuel_bottom & -fuel_top & +fuel_left & -fuel_right & -fuel_front & +fuel_back

fuel_cell = mc.Cell(region=fuel_region, fill=fuel)


clad_top = mc.ZPlane(z0=32.55)
clad_bottom = mc.ZPlane(z0=-32.55)
clad_right = mc.XPlane(x0=3.615)
clad_left = mc.XPlane(x0=-3.615)
clad_front = mc.YPlane(y0=0.0635)
clad_back = mc.YPlane(y0=-0.0635)

clad_region = (+clad_bottom & -clad_top & +clad_left & -clad_right &
               -clad_front & +clad_back & ~fuel_region)

clad_cell = mc.Cell(region=clad_region, fill=Al6061)


dummy_cell= mc.Cell(fill=Al6061, region= +clad_bottom & -clad_top & +clad_left &
                                         -clad_right & -clad_front & +clad_back)

screw_1_cylinder = mc.YCylinder(r= 1.2, x0= -3.615/2, z0= 31.275)
screw_2_cylinder = mc.YCylinder(r= 1.2, x0 = 3.615/2, z0= 31.275)
screw_3_cylinder = mc.YCylinder(r= 1.2, x0= -3.615/2, z0= -31.275)
screw_4_cylinder = mc.YCylinder(r= 1.2, x0=  3.615/2, z0= -31.275)



coolant_region = ~clad_region & ~fuel_region & +screw_1_cylinder & +screw_2_cylinder & +screw_3_cylinder & +screw_4_cylinder

coolant = mc.Cell(region=coolant_region, fill=water)
coolant_2 = mc.Cell(region=coolant_region, fill=water)



infinite_air = mc.Cell(fill = air)
infinite_air_universe = mc.Universe()
infinite_air_universe.add_cell(infinite_air)


infinite_water = mc.Cell(fill = water)
infinite_water_universe = mc.Universe()
infinite_water_universe.add_cell(infinite_water)

infinite_graphite_cell = mc.Cell(fill=graphite)
infinite_graphite_universe = mc.Universe(cells=[infinite_graphite_cell])

infinite_cladding = mc.Cell(fill=Al6061)
infinite_cladding_universe = mc.Universe(cells=[infinite_cladding])

infinite_barite_concrete = mc.Cell(fill=barite_concrete)
infinite_barite_concrete_universe = mc.Universe(cells=[infinite_barite_concrete])



screw_1 = mc.Cell(fill= Al6061, region= -screw_1_cylinder & ~fuel_region & ~ clad_region)
screw_2 = mc.Cell(fill= Al6061, region= -screw_2_cylinder & ~fuel_region & ~ clad_region)
screw_3 = mc.Cell(fill= Al6061, region= -screw_3_cylinder & ~fuel_region & ~ clad_region)
screw_4 = mc.Cell(fill= Al6061, region= -screw_4_cylinder & ~fuel_region & ~ clad_region)

screw_11 = mc.Cell(fill= Al6061, region= -screw_1_cylinder & ~fuel_region & ~clad_region)
screw_22 = mc.Cell(fill= Al6061, region= -screw_2_cylinder & ~fuel_region & ~clad_region)
screw_33 = mc.Cell(fill= Al6061, region= -screw_3_cylinder & ~fuel_region & ~clad_region)
screw_44 = mc.Cell(fill= Al6061, region= -screw_4_cylinder & ~fuel_region & ~clad_region)


fuel_plate = mc.Universe(cells=[fuel_cell, clad_cell, coolant, screw_1, screw_2, screw_3, screw_4])

dummy_plate= mc.Universe(cells=[dummy_cell, coolant_2, screw_11, screw_22, screw_33, screw_44])

#####################################################################################
#                                   FUEL ASSEMBLY                                   #
#####################################################################################

ASSEMBLY_LENGTH = 5.726

fuel_assembly = mc.RectLattice(name='fuel assembly')
fuel_assembly.lower_left = (-3.615, -2.863)
fuel_assembly.pitch = (7.23, 0.409)
fuel_assembly.universes = [[fuel_plate],
                           [fuel_plate],
                           [fuel_plate],
                           [fuel_plate],
                           [fuel_plate],
                           [fuel_plate],
                           [fuel_plate],
                           [fuel_plate],
                           [fuel_plate],
                           [fuel_plate],
                           [fuel_plate],
                           [fuel_plate],
                           [fuel_plate],
                           [fuel_plate]]

fuel_assembly.outer = infinite_water_universe
fuel_assembly_cell = mc.Cell()
fuel_assembly_cell.fill = fuel_assembly

dummy_assembly = mc.RectLattice(name='dummy assembly')
dummy_assembly.lower_left = (-3.615, -2.863)
dummy_assembly.pitch = (7.23, 0.409)
dummy_assembly.universes = [[dummy_plate],
                            [dummy_plate],
                            [dummy_plate],
                            [dummy_plate],
                            [dummy_plate],
                            [dummy_plate],
                            [dummy_plate],
                            [dummy_plate],
                            [dummy_plate],
                            [dummy_plate],
                            [dummy_plate],
                            [dummy_plate],
                            [dummy_plate],
                            [dummy_plate]]

dummy_assembly.outer = infinite_water_universe
dummy_assembly_cell = mc.Cell()
dummy_assembly_cell.fill = dummy_assembly

partial_dummy_assembly = mc.RectLattice(name='dummy assembly')
partial_dummy_assembly.lower_left = (-3.615, -2.863)
partial_dummy_assembly.pitch = (7.23, 0.409)
partial_dummy_assembly.universes = [[fuel_plate],
                                    [fuel_plate],
                                    [fuel_plate],
                                    [fuel_plate],
                                    [dummy_plate],
                                    [dummy_plate],
                                    [dummy_plate],
                                    [dummy_plate],
                                    [dummy_plate],
                                    [dummy_plate],
                                    [dummy_plate],
                                    [dummy_plate],
                                    [dummy_plate]]

partial_dummy_assembly.outer = infinite_water_universe
partial_dummy_assembly_cell = mc.Cell()
partial_dummy_assembly_cell.fill = partial_dummy_assembly

fuel_assembly_universe = mc.Universe()
fuel_assembly_universe.add_cell(fuel_assembly_cell)

dummy_assembly_universe = mc.Universe()
dummy_assembly_universe.add_cell(dummy_assembly_cell)

partial_dummy_assembly_universe = mc.Universe(cells=[partial_dummy_assembly_cell])





#####################################################################################
#                                     FUEL BOXES                                    #
#####################################################################################

fuel_box = mc.RectLattice(name = 'fuel box')
fuel_box.lower_left = (-8.01, -5.726 - 0.282)
fuel_box.pitch = (8.005, 5.726 + 0.282)

fuel_box.universes = [[fuel_assembly_universe, fuel_assembly_universe],
                      [fuel_assembly_universe, fuel_assembly_universe]]

fuel_box.outer = mc.Universe(cells=[mc.Cell(fill= water)], name='water surrounding fuel assembly lattice')
fuel_box_cell = mc.Cell()
fuel_box_cell.fill = fuel_box


right_box_inner_boundary = mc.XPlane(x0= 7.62)
left_box_inner_boundary = mc.XPlane(x0= -7.62)
front_box_inner_boundary = mc.YPlane(y0= 6.35)
back_box_inner_boundary = mc.YPlane(y0= -6.35)
top_box_inner_boundary = mc.ZPlane(z0= 60.95)
top_box_water_boundary = mc.ZPlane(z0= 60.95 - 5.08)
bottom_box_inner_boundary = mc.ZPlane(z0= -60.95)

right_box_outer_boundary = mc.XPlane(x0= 7.62 +0.318)
left_box_outer_boundary = mc.XPlane(x0= -7.62 -0.318)
front_box_outer_boundary = mc.YPlane(y0= 6.35 +0.318)
back_box_outer_boundary = mc.YPlane(y0= -6.35 -0.318)
top_box_outer_boundary = mc.ZPlane(z0= 60.95 +0.318)
bottom_box_outer_boundary = mc.ZPlane(z0= -60.95 -0.318)


fuel_box_dummy_1 = mc.RectLattice(name = 'fuel box with dummy assembly')
fuel_box_dummy_1.lower_left = (-8.01, -5.726 - 0.282)
fuel_box_dummy_1.pitch = (8.005, 5.726 + 0.282)

fuel_box_dummy_1.universes = [[fuel_assembly_universe, fuel_assembly_universe],
                            [fuel_assembly_universe, dummy_assembly_universe]]

fuel_box_dummy_1.outer = mc.Universe(cells=[mc.Cell(fill= water)], name='water surrounding fuel assembly lattice')
fuel_box_dummy_1_cell = mc.Cell()
fuel_box_dummy_1_cell.fill = fuel_box_dummy_1

fuel_box_dummy_2 = mc.RectLattice(name = 'fuel box with partial dummy assembly')
fuel_box_dummy_2.lower_left = (-8.01, -5.726 - 0.282)
fuel_box_dummy_2.pitch = (8.005, 5.726 + 0.282)

fuel_box_dummy_2.universes = [[fuel_assembly_universe, dummy_assembly_universe],
                                    [fuel_assembly_universe, fuel_assembly_universe]]

fuel_box_dummy_2.outer = mc.Universe(cells=[mc.Cell(fill= water)], name='water surrounding fuel assembly lattice')
fuel_box_dummy_2_cell = mc.Cell()
fuel_box_dummy_2_cell.fill = fuel_box_dummy_2



fuel_box_cell.region = (-right_box_inner_boundary & +left_box_inner_boundary & -front_box_inner_boundary
                        & +back_box_inner_boundary & -top_box_water_boundary & +bottom_box_inner_boundary)

fuel_box_air_region = (-right_box_inner_boundary & +left_box_inner_boundary & -front_box_inner_boundary &
                       +back_box_inner_boundary & +top_box_water_boundary & -top_box_inner_boundary)

fuel_box_wall_region = (-right_box_outer_boundary & +left_box_outer_boundary & -front_box_outer_boundary &
                        +back_box_outer_boundary & -top_box_outer_boundary & +bottom_box_outer_boundary &
                        ~fuel_box_cell.region & ~fuel_box_air_region)

fuel_box_wall = mc.Cell(fill=Al6061, region=fuel_box_wall_region)
fuel_box_wall_1 = mc.Cell(fill=Al6061, region=fuel_box_wall_region)
fuel_box_wall_2 = mc.Cell(fill=Al6061, region=fuel_box_wall_region)

fuel_box_air = mc.Cell(fill=air, region=fuel_box_air_region)
fuel_box_air_1 = mc.Cell(fill=air, region=fuel_box_air_region)
fuel_box_air_2 = mc.Cell(fill=air, region=fuel_box_air_region)

fuel_box_dummy_1_cell.region = fuel_box_cell.region
fuel_box_dummy_2_cell.region = fuel_box_cell.region


box_air = mc.Cell(fill=air, region= (~fuel_box_cell.region & ~fuel_box_wall_region))
box_air_1 = mc.Cell(fill=air, region= (~fuel_box_cell.region & ~fuel_box_wall_region))
box_air_2 = mc.Cell(fill=air, region= (~fuel_box_cell.region & ~fuel_box_wall_region))

fuel_box_universe = mc.Universe(cells=[fuel_box_cell, fuel_box_wall, fuel_box_air])
dummy_box_universe = mc.Universe(cells=[fuel_box_dummy_1_cell, fuel_box_wall_1, fuel_box_air_1])
partial_dummy_box_universe = mc.Universe(cells=[fuel_box_dummy_2_cell, fuel_box_wall_2, fuel_box_air_2])



fuel_box_1_cell = mc.Cell(fill= fuel_box_universe)
fuel_box_2_cell = mc.Cell(fill= fuel_box_universe)
fuel_box_3_cell = mc.Cell(fill= dummy_box_universe)
fuel_box_4_cell = mc.Cell(fill= fuel_box_universe)
fuel_box_5_cell = mc.Cell(fill= fuel_box_universe)
fuel_box_6_cell = mc.Cell(fill= partial_dummy_box_universe)

BOX_WIDTH = 15.876
BOX_LENGTH = 13.336
BOX_HEIGHT = 122.536


SHROUD_WIDTH = 2.54
SHROUD_LENGTH = 90.4
SHROUD_HEIGHT = 91.4

BOX_Y_SPACING = 30.48

SHROUD_X_SPACING = (BOX_WIDTH/2) + SHROUD_WIDTH/2
SHROUD_Y_SPACING = (SHROUD_LENGTH/2) + BOX_Y_SPACING/2 - 2.22


fuel_box_1_cell.translation = (-BOX_WIDTH - SHROUD_WIDTH, -(BOX_LENGTH/2)-(BOX_Y_SPACING/2), 0)

box_1_back = mc.YPlane(y0=- (BOX_LENGTH)-(BOX_Y_SPACING/2))
box_1_front = mc.YPlane(y0= -BOX_Y_SPACING/2)
box_1_right = mc.XPlane(x0=- BOX_WIDTH/2- SHROUD_WIDTH)
box_1_left = mc.XPlane(x0=- BOX_WIDTH/2 - SHROUD_WIDTH - BOX_WIDTH)

fuel_box_1_cell.region = (-box_1_right & +box_1_left & -box_1_front &
                          +box_1_back & -top_box_outer_boundary & +bottom_box_outer_boundary)




fuel_box_2_cell.translation = (0, -(BOX_LENGTH/2)-(BOX_Y_SPACING/2), 0)

box_2_back = box_1_back
box_2_front = box_1_front
box_2_right = right_box_outer_boundary
box_2_left = left_box_outer_boundary

fuel_box_2_cell.region = (-box_2_right & +box_2_left & -box_2_front &
                          +box_2_back & -top_box_outer_boundary & +bottom_box_outer_boundary)




fuel_box_3_cell.translation = (BOX_WIDTH + SHROUD_WIDTH, -(BOX_LENGTH/2)-(BOX_Y_SPACING/2), 0)

box_3_back = box_1_back
box_3_front = box_1_front
box_3_right = mc.XPlane(x0= BOX_WIDTH/2 + SHROUD_WIDTH + BOX_WIDTH)
box_3_left = mc.XPlane(x0= BOX_WIDTH/2 + SHROUD_WIDTH)

fuel_box_3_cell.region = (-box_3_right & +box_3_left & -box_3_front &
                          +box_3_back & -top_box_outer_boundary & +bottom_box_outer_boundary)




fuel_box_4_cell.translation = (-BOX_WIDTH - SHROUD_WIDTH, (BOX_LENGTH/2)+(BOX_Y_SPACING/2), 0)

box_4_back = mc.YPlane(y0= BOX_Y_SPACING/2)
box_4_front = mc.YPlane(y0= 28.576)
box_4_right = box_1_right
box_4_left = box_1_left

fuel_box_4_cell.region = (-box_4_right & +box_4_left & -box_4_front &
                          +box_4_back & -top_box_outer_boundary & +bottom_box_outer_boundary)




fuel_box_5_cell.translation = (0, (BOX_LENGTH/2)+(BOX_Y_SPACING/2), 0)

box_5_back = box_4_back
box_5_front = box_4_front
box_5_right = box_2_right
box_5_left = box_2_left

fuel_box_5_cell.region = (-box_5_right & +box_5_left & -box_5_front &
                          +box_5_back & -top_box_outer_boundary & +bottom_box_outer_boundary)




fuel_box_6_cell.translation = (BOX_WIDTH + SHROUD_WIDTH, (BOX_LENGTH/2)+(BOX_Y_SPACING/2), 0)

box_6_back = box_4_back
box_6_front = box_4_front
box_6_right = box_3_right
box_6_left = box_3_left

fuel_box_6_cell.region = (-box_6_right & +box_6_left & -box_6_front & +box_6_back
                           & -top_box_outer_boundary & +bottom_box_outer_boundary)





#####################################################################################
#                                 CONTROL BLADES                                    #
#####################################################################################

SHROUD_THICKNESS = (2.54-1.9)/2
SHROUD_X_INNER = 1.9
INCLINE_SLOPE = (34.3-10.8)/61.9
DECLINED_SLOPE = (27.9-34.3)/12.7
BLADE_THICKNESS = 0.259
Cd_THICKNESS = 0.102

shroud_inner_top = mc.ZPlane(z0=SHROUD_HEIGHT/2 - SHROUD_THICKNESS)
shroud_inner_bottom = mc.ZPlane(z0=-SHROUD_HEIGHT/2 + SHROUD_THICKNESS)
shroud_inner_front = mc.YPlane(y0=SHROUD_LENGTH/2 - SHROUD_THICKNESS)
shroud_inner_back = mc.YPlane(y0=-SHROUD_LENGTH/2 + SHROUD_THICKNESS)
shroud_inner_right = mc.XPlane(x0=SHROUD_X_INNER/2)
shroud_inner_left = mc.XPlane(x0=-SHROUD_X_INNER/2)

shroud_outer_top = mc.ZPlane(z0=SHROUD_HEIGHT/2)
shroud_outer_bottom = mc.ZPlane(z0=-SHROUD_HEIGHT/2)
shroud_outer_front = mc.YPlane(y0=SHROUD_LENGTH/2)
shroud_outer_back = mc.YPlane(y0=-SHROUD_LENGTH/2)
shroud_outer_right = mc.XPlane(x0=SHROUD_X_INNER/2 + SHROUD_THICKNESS)
shroud_outer_left = mc.XPlane(x0=-SHROUD_X_INNER/2 - SHROUD_THICKNESS)

shroud_inner_region = (-shroud_inner_top & +shroud_inner_bottom & -shroud_inner_front &
                       +shroud_inner_back & -shroud_inner_right & +shroud_inner_left)

shroud_outer_region = (-shroud_outer_top & +shroud_outer_bottom & -shroud_outer_front &
                       +shroud_outer_back & -shroud_outer_right & +shroud_outer_left)

shroud_region = shroud_outer_region & ~ shroud_inner_region

shroud_cell = mc.Cell(fill=magnesium, region= shroud_region)
shroud_universe = mc.Universe(cells= [shroud_cell])

shroud_cell_1 = mc.Cell(fill= shroud_universe, region= shroud_region)
shroud_cell_2 = mc.Cell(fill= shroud_universe, region= shroud_region)
shroud_cell_3 = mc.Cell(fill= shroud_universe, region= shroud_region)
shroud_cell_4 = mc.Cell(fill= shroud_universe, region= shroud_region)



# y and z surfaces are mutual for the whole blade, so both aluminum and cadmium share the same surfaces
blade_inclination = mc.Plane(a=0, b=-INCLINE_SLOPE, c=1, d=5.4)
blade_declination = mc.Plane(a=0, b= -DECLINED_SLOPE, c= 1, d= 76319/1270)
safety_blade_mid_interception = mc.YPlane(y0=61.9)
regulating_blade_mid_interception = mc.YPlane(y0= 61.9 + 12.7 - 4.57) # Regulating blades have lower amount of cadmium compared to safety blades
blade_bottom = mc.ZPlane(z0=-10.8/2)
blade_front = mc.YPlane(y0= 61.9+12.7)
blade_back = mc.YPlane(y0= 0)

# x surfaces are where the distinction happen between Cadmium and Aluminum
aluminum_outer_right = mc.XPlane(x0= BLADE_THICKNESS/2)
aluminum_outer_left = mc.XPlane(x0= -BLADE_THICKNESS/2)
aluminum_inner_right = mc.XPlane(x0= +Cd_THICKNESS/2)
aluminum_inner_left = mc.XPlane(x0= -Cd_THICKNESS/2)
test_upper = mc.ZPlane(z0= 35)

blade_region = (-blade_inclination & -blade_declination & + blade_bottom & + blade_back & -blade_front &
                    + aluminum_outer_left & -aluminum_outer_right)

safety_cadmium_region = (+safety_blade_mid_interception & -blade_front & -blade_declination &
                         +blade_bottom & -aluminum_inner_right & +aluminum_inner_left)

regulating_cadmium_region = (+regulating_blade_mid_interception & -blade_front & -blade_declination &
                         +blade_bottom & -aluminum_inner_right & +aluminum_inner_left)

safety_aluminum_blade_cell = mc.Cell(fill=Al6061, region= blade_region & ~safety_cadmium_region)

safety_cadmium_blade_cell = mc.Cell(fill=cadmium, region= safety_cadmium_region)


regulating_aluminum_blade_cell = mc.Cell(fill=Al6061, region= blade_region & ~regulating_cadmium_region)

regulating_cadmium_blade_cell = mc.Cell(fill=cadmium, region= regulating_cadmium_region)



safety_blade_universe = mc.Universe(cells=[safety_aluminum_blade_cell, safety_cadmium_blade_cell])

regulating_blade_universe = mc.Universe(cells=[regulating_aluminum_blade_cell, regulating_cadmium_blade_cell])


'''
now we have to create three cells for each of the safety blades, the reason for creating them like this is that we
have to have the ability to apply methods on the specific cell to withdraw it, as it is with draw in vertical rotation
'''
safety_blade_1_temporary_cell = mc.Cell(fill= safety_blade_universe, region= blade_region)
safety_blade_2_temporary_cell = mc.Cell(fill= safety_blade_universe, region= blade_region)
safety_blade_3_temporary_cell = mc.Cell(fill= safety_blade_universe, region= blade_region)
regulating_blade_temporary_cell = mc.Cell(fill= regulating_blade_universe, region= blade_region)

'''
now we need to apply translation to each cell to make the center of the cell the origin of 
rotation, then apply rotation, then add them to a universe then to their individual final cell 
'''



safety_blade_1_universe = mc.Universe(cells=[safety_blade_1_temporary_cell, mc.Cell(fill=air, region=~blade_region)])
safety_blade_1_rotation_cell = mc.Cell(fill= safety_blade_1_universe)

safety_blade_2_universe = mc.Universe(cells=[safety_blade_2_temporary_cell, mc.Cell(fill=air, region=~blade_region)])
safety_blade_2_rotation_cell = mc.Cell(fill= safety_blade_2_universe)

safety_blade_3_universe = mc.Universe(cells=[safety_blade_3_temporary_cell, mc.Cell(fill=air, region=~blade_region)])
safety_blade_3_rotation_cell = mc.Cell(fill= safety_blade_3_universe)

regulating_blade_universe = mc.Universe(cells=[regulating_blade_temporary_cell, mc.Cell(fill=air, region=~blade_region)])
regulating_blade_rotation_cell = mc.Cell(fill= regulating_blade_universe)



#######################################################################################################################################################
#######################################################################################################################################################
'''
BLADE INSERTION AND WITHDRAWAL:
 
Blades rotate is between 0 and 45 degrees, 0 being fully inserted, 1000 being fully withdrawn. But in the control room, it 
is normalized out of 1000, 1000 being fully withdrawn which corresponds to 45 degrees, and 0 being fully inserted  corresponding to 0 degrees

The function below will handle rotation of blades and can take units of exactly as observed in the control room (0-1000) or degrees or in degrees (0-45)

The critical position of UFTR corresponding to this fresh core model was ====> Safety Blades 1,2,3 = 570 ---- Regulating Blade = 325 
'''
#######################################################################################################################################################
#######################################################################################################################################################

def set_control_blades_positions(SB1, SB2, SB3, RB, unit):
    if unit == "degrees":
        safety_blade_1_rotation_cell.rotation = (SB1, 0, 0)

        safety_blade_2_rotation_cell.rotation = (SB2, 0, 0)

        safety_blade_3_rotation_cell.rotation = (SB3, 0, 0)

        regulating_blade_rotation_cell.rotation = (RB, 0, 0)

    if unit == "control room 0-1000 units":
        safety_blade_1_rotation_cell.rotation = ((SB1 * 0.045), 0,0)

        safety_blade_2_rotation_cell.rotation = ((SB2 * 0.045), 0,0)

        safety_blade_3_rotation_cell.rotation = ((SB3 * 0.045), 0,0)

        regulating_blade_rotation_cell.rotation = ((RB * 0.045), 0,0)


def verify_control_blades_positions(blades, max_angle=45):
    blades = [safety_blade_1_rotation_cell, safety_blade_2_rotation_cell,
              safety_blade_3_rotation_cell, regulating_blade_rotation_cell]
    for blade in blades:
        x, y, z = blade.rotation

        if not 0 <= x <= max_angle:
            raise ValueError(f"Rotation of {blade} must be between 0 and 1000 units, corresponding to rotation between 0 and 45 degrees")

        if y != 0 or z != 0:
            raise ValueError(f"{blade} has invalid Y/Z rotation: ({y}, {z}), they must both be 0, the correct rotation axis is x")

#######################################################################################################################################################
#######################################################################################################################################################


# Now translating blades back into their actual position inside the shroud

safety_blade_1_rotation_cell.translation = (0,-34.8, -27.9)
safety_blade_2_rotation_cell.translation = (0,-34.8, -27.9)
safety_blade_3_rotation_cell.translation = (0,-34.8, -27.9)
regulating_blade_rotation_cell.translation = (0,-34.8, -27.9)


safety_blade_1_rotation_cell.region = shroud_inner_region

safety_blade_1_universe = mc.Universe(cells=[shroud_cell_1, safety_blade_1_rotation_cell])
safety_blade_1_cell = mc.Cell(fill=safety_blade_1_universe)

safety_blade_1_cell.translation = (SHROUD_X_SPACING, -SHROUD_Y_SPACING, 25.568)

blade_1_back = mc.YPlane(y0= (-BOX_Y_SPACING/2)+2.22-SHROUD_LENGTH)
blade_1_front = mc.YPlane(y0= (-BOX_Y_SPACING/2)+2.22)
blade_1_bottom = mc.ZPlane(z0= -20.132)
blade_1_top = mc.ZPlane(z0= 71.268)
blade_1_right = box_2_right
blade_1_left = box_3_left


safety_blade_1_cell.region = (+blade_1_right & - blade_1_left & +blade_1_back &
                              -blade_1_front & - blade_1_top & + blade_1_bottom)




safety_blade_2_rotation_cell.region = shroud_inner_region

safety_blade_2_universe = mc.Universe(cells=[shroud_cell_2, safety_blade_2_rotation_cell])
safety_blade_2_cell = mc.Cell(fill=safety_blade_2_universe)

safety_blade_2_cell.translation = (-SHROUD_X_SPACING, -SHROUD_Y_SPACING, 25.568)

blade_2_back = blade_1_back
blade_2_front = blade_1_front
blade_2_bottom = blade_1_bottom
blade_2_top = blade_1_top
blade_2_right = box_1_right
blade_2_left = box_2_left

safety_blade_2_cell.region = (+blade_2_right & -blade_2_left & +blade_2_back &
                              -blade_2_front & - blade_2_top & + blade_2_bottom)




safety_blade_3_rotation_cell.region = shroud_inner_region

safety_blade_3_universe = mc.Universe(cells=[shroud_cell_3, safety_blade_3_rotation_cell])
safety_blade_3_cell = mc.Cell(fill=safety_blade_3_universe)

safety_blade_3_cell.rotation = (0,0,180)
safety_blade_3_cell.translation = (-SHROUD_X_SPACING, SHROUD_Y_SPACING, 25.568)

blade_3_back = mc.YPlane(y0= (BOX_Y_SPACING/2)-2.22+SHROUD_LENGTH)
blade_3_front = mc.YPlane(y0= (BOX_Y_SPACING/2)-2.22)
blade_3_bottom = blade_1_bottom
blade_3_top = blade_1_top
blade_3_right = box_5_left
blade_3_left = box_4_right

safety_blade_3_cell.region = (-blade_3_back & +blade_3_front & + blade_3_bottom &
                              - blade_3_top & -blade_3_right & +blade_3_left)



regulating_blade_rotation_cell.region = shroud_inner_region

regulating_blade_universe = mc.Universe(cells=[shroud_cell_4, regulating_blade_rotation_cell])
regulating_blade_cell = mc.Cell(fill=regulating_blade_universe)

regulating_blade_cell.rotation = (0,0,180)
regulating_blade_cell.translation = (SHROUD_X_SPACING, SHROUD_Y_SPACING, 25.568)



regulating_blade_back = blade_3_back
regulating_blade_front = blade_3_front
regulating_blade_bottom = blade_1_bottom
regulating_blade_top = blade_1_top
regulating_blade_right = box_6_left
regulating_blade_left = box_5_right

regulating_blade_cell.region = (-regulating_blade_back & +regulating_blade_front & + regulating_blade_bottom
                                & -regulating_blade_top & -regulating_blade_right & +regulating_blade_left)




#####################################################################################
#                                REST OF THE GEOMETRY                               #
#####################################################################################

CORE_HEIGHT = 5 * 30.48
CORE_LENGTH = 5 * 30.48
CORE_WIDTH = 5 * 30.48

core_left = mc.XPlane(x0=-CORE_WIDTH / 2)
core_right = mc.XPlane(x0=264.16 - (CORE_WIDTH / 2))
core_back = mc.YPlane(y0=-CORE_LENGTH / 2)
core_front = mc.YPlane(y0=CORE_LENGTH / 2)
core_bottom = bottom_box_outer_boundary
core_top = top_box_outer_boundary

thermal_column_cylinder_1 = mc.XCylinder(y0=0, z0=0, r=10)
thermal_column_cylinder_2 = mc.XCylinder(y0=35, z0=0, r=5)
thermal_column_cylinder_3 = mc.XCylinder(y0=-35, z0=0, r=5)
thermal_column_right = mc.XPlane(x0=(BOX_Y_SPACING * (37 / 6)))
thermal_column_left = mc.XPlane(x0=CORE_WIDTH / 2)

thermal_column_cell_1 = mc.Cell(fill=air, region=(-thermal_column_cylinder_1 &
                                                  -thermal_column_right & +thermal_column_left))

core_region = (+core_left & -core_right & +core_back & -core_front & +core_bottom & -core_top &
               ~thermal_column_cell_1.region)

north_air_left = core_left
north_air_right = mc.XPlane(x0=CORE_WIDTH / 2)
north_air_back = core_front
north_air_front = mc.YPlane(y0=(CORE_LENGTH / 2) + 20.32)
north_air_bottom = core_bottom
north_air_top = core_top

north_air_region = (+north_air_left & -north_air_right & +north_air_back & -north_air_front &
                    +north_air_bottom & -north_air_top & ~safety_blade_3_cell.region & ~regulating_blade_cell.region)

south_air_left = core_left
south_air_right = north_air_right
south_air_back = mc.YPlane(y0=-(CORE_LENGTH / 2) - 20.32)
south_air_front = core_back
south_air_bottom = core_bottom
south_air_top = core_top

south_air_region = (+south_air_left & -south_air_right & +south_air_back & -south_air_front &
                    +south_air_bottom & -south_air_top & ~safety_blade_1_cell.region & ~safety_blade_2_cell.region)

core_air_cell = mc.Cell(fill=air, region=north_air_region | south_air_region)

central_vertical_port_cylinder = mc.ZCylinder(x0=0, y0=0, r=3)
west_vertical_port_cylinder = mc.ZCylinder(x0=-20, y0=0, r=3)
east_vertical_port_cylinder = mc.ZCylinder(x0=20, y0=0, r=3)
vertical_port_top = mc.ZPlane(z0=60.95 + 0.318 + 25.4 + 152.4)
vertical_port_bottom = mc.ZPlane(z0=50)

central_vertical_port_cell = mc.Cell(fill=air, region=(-central_vertical_port_cylinder &
                                                       -vertical_port_top & +vertical_port_bottom))

west_vertical_port_cell = mc.Cell(fill=air, region=(-west_vertical_port_cylinder &
                                                    -vertical_port_top & +vertical_port_bottom))
east_vertical_port_cell = mc.Cell(fill=air, region=(-east_vertical_port_cylinder &
                                                    -vertical_port_top & +vertical_port_bottom))

rabit_tube_cylinder = mc.XCylinder(y0=0, z0=0, r=3)
rabit_tube_right = mc.XPlane(x0=11)
rabit_tube_left = mc.XPlane(x0=-(BOX_Y_SPACING * 7.5) - 101.6)

rabit_tube_cell = mc.Cell(fill=air, region=-rabit_tube_cylinder & -rabit_tube_right & +rabit_tube_left)

graphite_cell_1 = mc.Cell(fill=graphite, region=(core_region & ~fuel_box_1_cell.region & ~fuel_box_2_cell.region &
                                                 ~fuel_box_3_cell.region & ~fuel_box_4_cell.region &
                                                 ~fuel_box_5_cell.region & ~fuel_box_6_cell.region &
                                                 ~safety_blade_1_cell.region & ~safety_blade_2_cell.region &
                                                 ~safety_blade_3_cell.region & ~regulating_blade_cell.region &
                                                 ~thermal_column_cell_1.region & ~rabit_tube_cell.region &
                                                 ~west_vertical_port_cell.region &
                                                 ~east_vertical_port_cell.region &
                                                 ~central_vertical_port_cell.region))

extra_graphite_left = mc.XPlane(x0=-BOX_Y_SPACING * (4 / 3))
extra_graphite_right = mc.XPlane(x0=BOX_Y_SPACING * (4 / 3))
extra_graphite_back = mc.YPlane(y0=-BOX_Y_SPACING * (4 / 3))
extra_graphite_front = mc.YPlane(y0=BOX_Y_SPACING * (4 / 3))
extra_graphite_bottom = core_top
extra_graphite_top = mc.ZPlane(z0=60.95 + 20.32)

graphite_cell_2 = mc.Cell(fill=graphite, region=(+extra_graphite_left & -extra_graphite_right &
                                                 +extra_graphite_back & -extra_graphite_front &
                                                 +extra_graphite_bottom & -extra_graphite_top &
                                                 ~thermal_column_cell_1.region & ~rabit_tube_cell.region &
                                                 ~west_vertical_port_cell.region & ~east_vertical_port_cell.region &
                                                 ~central_vertical_port_cell.region & ~safety_blade_1_cell.region &
                                                 ~safety_blade_2_cell.region & ~safety_blade_3_cell.region &
                                                 ~regulating_blade_cell.region))

water_tank_right = core_left
water_tank_left = mc.XPlane(x0=-228.6)
water_tank_top = mc.ZPlane(z0=350.52)
water_tank_bottom = core_bottom
water_tank_front = core_front
water_tank_back = core_back

water_tank_region = (-water_tank_right & + water_tank_left & - water_tank_top &
                     + water_tank_bottom & - water_tank_front & + water_tank_back)

water_tank_cell = mc.Cell(fill=water, region=water_tank_region & ~ core_region & ~rabit_tube_cell.region)

concrete_top = vertical_port_top
concrete_bottom = mc.ZPlane(z0=-182.88)
concrete_right = mc.XPlane(x0=(BOX_Y_SPACING * (37 / 6)) + 101.6)
concrete_left = rabit_tube_left
concrete_front = mc.YPlane(y0=279.4)
concrete_back = mc.YPlane(y0=-279.4)

concrete_region = -concrete_top & +concrete_bottom & -concrete_right & +concrete_left & -concrete_front & +concrete_back

concrete_filling = mc.Cell(fill=barite_concrete, region=(concrete_region & ~core_region &
                                                         ~fuel_box_1_cell.region & ~fuel_box_2_cell.region &
                                                         ~fuel_box_3_cell.region & ~fuel_box_4_cell.region &
                                                         ~fuel_box_5_cell.region & ~fuel_box_6_cell.region &
                                                         ~safety_blade_1_cell.region & ~safety_blade_2_cell.region &
                                                         ~safety_blade_3_cell.region & ~regulating_blade_cell.region &
                                                         ~graphite_cell_2.region & ~water_tank_region &
                                                         ~core_air_cell.region & ~thermal_column_cell_1.region &
                                                         ~central_vertical_port_cell.region & ~west_vertical_port_cell.region &
                                                         ~east_vertical_port_cell.region & ~rabit_tube_cell.region))

air_filling_cell = mc.Cell(fill=air, region=(~concrete_region & ~core_region &
                                             ~fuel_box_1_cell.region & ~fuel_box_2_cell.region &
                                             ~fuel_box_3_cell.region & ~fuel_box_4_cell.region &
                                             ~fuel_box_5_cell.region & ~fuel_box_6_cell.region &
                                             ~safety_blade_1_cell.region & ~safety_blade_2_cell.region &
                                             ~safety_blade_3_cell.region & ~regulating_blade_cell.region &
                                             ~graphite_cell_2.region & ~water_tank_region &
                                             ~core_air_cell.region & ~thermal_column_cell_1.region &
                                             ~central_vertical_port_cell.region & ~west_vertical_port_cell.region &
                                             ~east_vertical_port_cell.region & ~rabit_tube_cell.region))

final_universe = mc.Universe(cells=[safety_blade_1_cell, safety_blade_2_cell, safety_blade_3_cell,
                                    regulating_blade_cell, fuel_box_1_cell, fuel_box_2_cell, fuel_box_3_cell,
                                    fuel_box_4_cell, fuel_box_5_cell, fuel_box_6_cell, graphite_cell_1,
                                    graphite_cell_2, concrete_filling, water_tank_cell, core_air_cell,
                                    thermal_column_cell_1,
                                    central_vertical_port_cell, west_vertical_port_cell,
                                    east_vertical_port_cell, rabit_tube_cell, air_filling_cell])

top = mc.ZPlane(z0=400, boundary_type='vacuum')
bottom = mc.ZPlane(z0=-200, boundary_type='vacuum')
right = mc.XPlane(x0=300, boundary_type='vacuum')
left = mc.XPlane(x0=-350, boundary_type='vacuum')
front = mc.YPlane(y0=300, boundary_type='vacuum')
back = mc.YPlane(y0=-300, boundary_type='vacuum')

final_cell = mc.Cell(fill=final_universe, region=-top & +bottom & -right & +left & -front & +back)

root_universe = mc.Universe(cells=[final_cell])

geometry = mc.Geometry(root_universe)






######################################################################################
#                                   MESHES & TALLIES                                 #
######################################################################################
def include_tallies():

    """
    # BOX_Y_SPACING
    # BOX_WIDTH
    # BOX_LENGTH
    # SHROUD_WIDTH
    # FUEL_WIDTH
    # ASSEMBLY_LENGTH
    BOX_WALL = 0.318
    WATER_SPACING = 0.282
    EXTRA_CLAD = 3.615 - 2.98


    # verified
    X1L = -(BOX_WIDTH/2) - SHROUD_WIDTH - BOX_WIDTH + BOX_WALL + EXTRA_CLAD
    Y1L = -(BOX_Y_SPACING/2) - BOX_LENGTH + BOX_WALL + (WATER_SPACING/2)
    X1U = -(BOX_WIDTH/2) - SHROUD_WIDTH - EXTRA_CLAD - BOX_WALL
    Y1U = -(BOX_Y_SPACING/2) - BOX_WALL - (WATER_SPACING/2)

    # verified
    X2L = -(BOX_WIDTH/2) + EXTRA_CLAD + BOX_WALL
    Y2L = Y1L
    X2U = (BOX_WIDTH/2) - EXTRA_CLAD - BOX_WALL
    Y2U = Y1U

    # verified
    X3L = (BOX_WIDTH/2) + SHROUD_WIDTH + BOX_WALL + EXTRA_CLAD
    Y3L = Y1L
    X3U = (BOX_WIDTH/2) + SHROUD_WIDTH + BOX_WIDTH - BOX_WALL - EXTRA_CLAD
    Y3U = Y1U


    X4L = X1L
    Y4L = (BOX_Y_SPACING/2) + BOX_WALL + (WATER_SPACING/2)
    X4U = X1U
    Y4U = (BOX_Y_SPACING/2) + BOX_LENGTH - BOX_WALL - (WATER_SPACING/2)

    X5L = X2L
    Y5L = Y4L
    X5U = X2U
    Y5U = Y4U

    X6L = X3L
    Y6L = Y4L
    X6U = X3U
    Y6U = Y4U


    ZL = -30.01
    ZU = 30.01



    box_1_mesh_filter = mc.RegularMesh()
    box_1_mesh_filter.lower_left = (X1L, Y1L, ZL)

    box_1_mesh_filter.upper_right = (X1U, Y1U, ZU)

    box_1_mesh_filter.dimension = (2, 2, 1)

    box_1_mesh = mc.MeshFilter(box_1_mesh_filter)

    box_1_tally = mc.Tally(name = 'box 1 power')
    box_1_tally.filters = [box_1_mesh]
    box_1_tally.scores=['fission', 'flux', 'fission-q-recoverable']



    box_2_mesh_filter = mc.RegularMesh()
    box_2_mesh_filter.lower_left = (X2L, Y2L, ZL)

    box_2_mesh_filter.upper_right = (X2U, Y2U, ZU)

    box_2_mesh_filter.dimension = (2, 2, 1)

    box_2_mesh = mc.MeshFilter(box_2_mesh_filter)

    box_2_tally = mc.Tally(name = 'box 2 power')
    box_2_tally.filters = [box_2_mesh]
    box_2_tally.scores=['fission', 'flux', 'fission-q-recoverable']



    box_3_mesh_filter = mc.RegularMesh()
    box_3_mesh_filter.lower_left = (X3L, Y3L, ZL)

    box_3_mesh_filter.upper_right = (X3U, Y3U, ZU)

    box_3_mesh_filter.dimension = (2, 2, 1)

    box_3_mesh = mc.MeshFilter(box_3_mesh_filter)

    box_3_tally = mc.Tally(name = 'box 3 power')
    box_3_tally.filters = [box_3_mesh]
    box_3_tally.scores=['fission', 'flux', 'fission-q-recoverable']



    box_4_mesh_filter = mc.RegularMesh()
    box_4_mesh_filter.lower_left = (X4L, Y4L, ZL)

    box_4_mesh_filter.upper_right = (X4U, Y4U, ZU)

    box_4_mesh_filter.dimension = (2, 2, 1)

    box_4_mesh = mc.MeshFilter(box_4_mesh_filter)

    box_4_tally = mc.Tally(name = 'box 4 power')
    box_4_tally.filters = [box_4_mesh]
    box_4_tally.scores=['fission', 'flux', 'fission-q-recoverable']




    box_5_mesh_filter = mc.RegularMesh()
    box_5_mesh_filter.lower_left = (X5L, Y5L, ZL)

    box_5_mesh_filter.upper_right = (X5U, Y5U, ZU)

    box_5_mesh_filter.dimension = (2, 2, 1)

    box_5_mesh = mc.MeshFilter(box_5_mesh_filter)

    box_5_tally = mc.Tally(name = 'box 5 power')
    box_5_tally.filters = [box_5_mesh]
    box_5_tally.scores=['fission', 'flux', 'fission-q-recoverable']



    box_6_mesh_filter = mc.RegularMesh()
    box_6_mesh_filter.lower_left = (X6L, Y6L, ZL)

    box_6_mesh_filter.upper_right = (X6U, Y6U, ZU)

    box_6_mesh_filter.dimension = (2, 2, 1)

    box_6_mesh = mc.MeshFilter(box_6_mesh_filter)

    box_6_tally = mc.Tally(name = 'box 6 power')
    box_6_tally.filters = [box_6_mesh]
    box_6_tally.scores=['fission', 'flux', 'fission-q-recoverable']


    material_filter = mc.MaterialFilter([1,2,3,4,5,6,7,8])

    generation_time_tally = mc.Tally(name = 'generation time tallies')
    generation_time_tally.filters = [material_filter]
    generation_time_tally.scores =['inverse-velocity', 'flux', 'absorption', 'prompt-nu-fission', 'fission']

    independent_inverse_velocity_tally = mc.Tally(name = 'generation time tallies')
    independent_inverse_velocity_tally.scores = ['inverse-velocity']


    # (300/3000) * (210/2100) * 60


    core_mesh_filter_1 = openmc.RegularMesh()
    core_mesh_filter_1.lower_left = (-100, -105, -30)
    core_mesh_filter_1.upper_right = (200, 105, 30)
    core_mesh_filter_1.dimension = (2100, 3000, 1)
    core_mesh = openmc.MeshFilter(core_mesh_filter_1)

    energies = np.logspace(np.log10(1e-3), np.log10(20.0e6), 51)
    e_filter = mc.EnergyFilter(energies)

    energy_tally = mc.Tally(name='spectrum')
    energy_tally.filters = [e_filter]
    energy_tally.scores = ['flux']


    energies = np.logspace(np.log10(1e-3), np.log10(20.0e6), 5001)
    e_filter = mc.EnergyFilter(energies)

    m_filter = mc.MaterialFilter([fuel, water, graphite, cadmium])

    materials_flux_tally = mc.Tally(name='materials flux')
    materials_flux_tally.scores = ['flux']
    materials_flux_tally.filters = [e_filter, m_filter]

    total_flux_tally = mc.Tally(name='total flux')
    total_flux_tally.scores = ['flux']
    total_flux_tally.filters = [e_filter]

    prompt_E_edges = np.geomspace(20, 20e6, 1201)
    prompt_chai_tally = mc.Tally(name='prompt watt spectrum')
    prompt_chai_tally.filters = [mc.EnergyoutFilter(prompt_E_edges)]
    prompt_chai_tally.scores  = ['nu-fission', 'prompt-nu-fission', 'delayed-nu-fission']

    delayed_E_edges = np.geomspace(20, 20e6, 601)
    delayed_chai_tally = mc.Tally(name='delayed watt spectrum')
    delayed_chai_tally.filters = [mc.EnergyoutFilter(delayed_E_edges)]
    delayed_chai_tally.scores  = ['nu-fission', 'delayed-nu-fission']


    radial_flux_mesh = mc.RegularMesh()
    radial_flux_mesh.lower_left = (-100, -5, -5)
    radial_flux_mesh.upper_right = (100,  5,  5)
    radial_flux_mesh.dimension = (2001, 1, 1)

    axial_flux_mesh = mc.RegularMesh()
    axial_flux_mesh.lower_left = (-5, -5, -100)
    axial_flux_mesh.upper_right =( 5,  5,  100)
    axial_flux_mesh.dimension = (1, 1, 2001)

    radial_flux_tally = mc.Tally(name= 'radial_flux')
    radial_flux_tally.filters = [mc.MeshFilter(radial_flux_mesh)]
    radial_flux_tally.scores = ['flux']

    axial_flux_tally = mc.Tally(name='axial_flux')
    axial_flux_tally.filters = [mc.MeshFilter(axial_flux_mesh)]
    axial_flux_tally.scores = ['flux']
    """
    core_mesh_filter_1 = openmc.RegularMesh()
    core_mesh_filter_1.lower_left = (-100, -105, -30)
    core_mesh_filter_1.upper_right = (200, 105, 30)
    core_mesh_filter_1.dimension = (2100, 3000, 1)
    core_mesh_1 = openmc.MeshFilter(core_mesh_filter_1)

    core_mesh = openmc.RegularMesh()
    core_mesh.lower_left = (-1, -1, -1)
    core_mesh.upper_right = (0, 0, 0)
    core_mesh.dimension = (1, 1, 1)
    core_mesh_filter = openmc.MeshFilter(core_mesh)

    tight_core_mesh = openmc.RegularMesh()
    tight_core_mesh.lower_left = (-45, -45, -30)
    tight_core_mesh.upper_right = (45, 45, 30)
    tight_core_mesh.dimension = (2000, 2000, 1)
    tight_core_mesh_filter = openmc.MeshFilter(tight_core_mesh)
    """
    core_mesh_filter_2 = openmc.RegularMesh()
    core_mesh_filter_2.lower_left = (-50, -50, -50)
    core_mesh_filter_2.upper_right = (50, 50, 30)
    core_mesh_filter_2.dimension = (5000, 5000, 1)
    core_mesh_2 = openmc.MeshFilter(core_mesh_filter_2)



    scatter_absorb_fission_tally = mc.Tally(name='scatter_absorb_fission')
    scatter_absorb_fission_tally.filters = [core_mesh_2]
    scatter_absorb_fission_tally.scores = ['absorption', 'scatter', 'total', 'fission']
    """
    thermal_energy = (0, 0.5)
    thermal_energy_filter = openmc.EnergyFilter(thermal_energy)

    epithermal_energy = (0.5, 20e6)
    epithermal_energy_filter = openmc.EnergyFilter(epithermal_energy)

    thermal_flux_tally = mc.Tally(name='thermal_flux')
    thermal_flux_tally.filters = [tight_core_mesh_filter, thermal_energy_filter]
    thermal_flux_tally.scores = ['flux']

    epithermal_flux_tally = mc.Tally(name='epithermal_flux')
    epithermal_flux_tally.filters = [core_mesh_filter, epithermal_energy_filter]
    epithermal_flux_tally.scores = ['flux']

    flux_normalization_tally = mc.Tally(name='flux_normalization')
    flux_normalization_tally. scores = ['flux', 'fission', 'heating', 'fission-q-recoverable', 'kappa-fission',
                                        'prompt-nu-fission', 'delayed-nu-fission', 'nu-fission']
    """
    energy_groups_50   = np.logspace(np.log10(1e-3), np.log10(20.0e6), 51)
    energy_groups_500  = np.logspace(np.log10(1e-3), np.log10(20.0e6), 501)
    energy_groups_5000 = np.logspace(np.log10(1e-3), np.log10(20.0e6), 5001)

    energy_groups_50_filter = mc.EnergyFilter(energy_groups_50)
    energy_groups_500_filter = mc.EnergyFilter(energy_groups_500)
    energy_groups_5000_filter = mc.EnergyFilter(energy_groups_5000)

    energy_spectrum_mesh = mc.RegularMesh()
    energy_spectrum_mesh.lower_left = (-9, -5, -5)
    energy_spectrum_mesh.upper_right = (1, 5, 5)
    energy_spectrum_mesh.dimension = (1,1,1)
    energy_spectrum_mesh_filter = mc.MeshFilter(energy_spectrum_mesh)

    energy_spectrum_50_tally = mc.Tally(name='energy_spectrum_50')
    energy_spectrum_50_tally.filters = [energy_spectrum_mesh_filter, energy_groups_50_filter]
    energy_spectrum_50_tally.scores = ['flux']

    energy_spectrum_500_tally = mc.Tally(name='energy_spectrum_500')
    energy_spectrum_500_tally.filters = [energy_spectrum_mesh_filter, energy_groups_500_filter]
    energy_spectrum_500_tally.scores = ['flux']

    energy_spectrum_5000_tally = mc.Tally(name='energy_spectrum_5000')
    energy_spectrum_5000_tally.filters = [energy_spectrum_mesh_filter, energy_groups_5000_filter]
    energy_spectrum_5000_tally.scores = ['flux']
    """
    tallies = mc.Tallies([thermal_flux_tally, flux_normalization_tally])
    tallies.export_to_xml()

#####################################################################################
#                                   SETTINGS & RUN                                  #
#####################################################################################

settings = mc.Settings()
settings.run_mode = 'eigenvalue'

# choose the desired control blades positions using on the function below, commented are some configurations you can uncomment that correspond to different conditions


set_control_blades_positions(SB1 = 720, SB2 = 720, SB3 = 720, RB = 325, unit= 'control room 0-1000 units') # 1st experimental critical configuration

# set_control_blades_positions(SB1 = 32.4, SB2 = 32.4, SB3 = 32.4, RB = 14.625, unit= 'degrees') # 1st experimental critical configuration in degrees

# set_control_blades_positions(SB1 = 675, SB2 = 675, SB3 = 675, RB = 415, unit= 'control room 0-1000 units') # 2nd experimental critical configuration

# set_control_blades_positions(SB1 = 625, SB2 = 625, SB3 = 625, RB = 380, unit= 'control room 0-1000 units') # 3rd experimental critical configuration

# set_control_blades_positions(SB1 = 660, SB2 = 660, SB3 = 660, RB = 466, unit= 'control room 0-1000 units') # MCNP critical configuration

#set_control_blades_positions(SB1 = 1000, SB2 = 1000, SB3 = 1000, RB = 1000, unit= 'control room 0-1000 units') # excess reactivity configuration

# set_control_blades_positions(SB1 = 0, SB2 = 0, SB3 = 1000, RB = 0, unit= 'control room 0-1000 units') # shutdown margin configuration



verify_control_blades_positions([safety_blade_1_rotation_cell, safety_blade_2_rotation_cell,
                                 safety_blade_3_rotation_cell, regulating_blade_rotation_cell])

# when being set at false, the run will estimate K only considering prompt neutrons, completely neglecting delayed neutrons
# to estimate Delayed neutron fraction, run once withe settings.create_delayed_neutrons = False and one without calling it, and subtract
# settings.create_delayed_neutrons = False

source = mc.Source()
source.space = mc.stats.Point((0.0, 22, 0.0)) # exactly in the middle of the fuel box with the highest expected flux
source.angle = mc.stats.Isotropic()
settings.energy_mode = ('continuous-energy')
settings.source = source

entropy_mesh = mc.RegularMesh()
entropy_mesh.lower_left = (-28.0, -29.01, -30.02)
entropy_mesh.upper_right = (28.0, 29.01, 30.02)
entropy_mesh.dimension = (7, 143, 1)

# when being set at false, the run will estimate K only considering prompt neutrons, completely neglecting delayed neutrons
# to estimate Delayed neutron fraction, run once withe settings.create_delayed_neutrons = False and one without calling it, and subtract
settings.create_delayed_neutrons = True

settings.batches = 535
settings.inactive = 35
# 500,000 particles at 500 batches with 100 inactive will produce approximately 7 pcm error and will take approximately 3 hours to run
settings.particles = 2000000 # multiply by 4 to reduce the error to half, multiply the 4 by 4 to reduce to another half, and so on
settings.entropy_mesh = entropy_mesh
settings.output = {'tallies': False, 'summary': False}

'''
settings.temperature = {"default": 296, "method": "interpolation", "range": (296, 312)} # temperature dependance is ignored due to:
1- negligible thermal effects at UFTR core
2- all experimental data the model is benchmarked against is done at a power level so low that it completely eliminates any temperature effects
'''


fresh_core_model = mc.Model(geometry=geometry, materials=materials, settings=settings)
if __name__ == "__main__":
    materials.export_to_xml()
    geometry.export_to_xml()
    # include_tallies()
    settings.export_to_xml()
    mc.run()