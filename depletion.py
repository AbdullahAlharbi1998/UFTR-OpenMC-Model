import openmc as mc
import openmc.deplete
from fresh_core import fresh_core_model

mc.config['cross_sections'] = 'please provide the path to your cross_sections.xml file in your system'
# The cross-sections library used in this model was ENDF/B-VIII.0
# It can be downloaded using this link: https://openmc.org/official-data-libraries/

op = mc.deplete.CoupledOperator(fresh_core_model,'please provide the path to your chain.xml file in your system')
# this has to be a unique library for depletion analysis
# ENDF has one that can be found here: https://openmc.org/depletion-chains/, look for ENDF/B-VIII.0 Chain (Thermal Spectrum)

TIME = [608, 2311, 2648] # days
POWER = [969.6, 0, 888.7] # Watts

integrator = openmc.deplete.CECMIntegrator(op, TIME, POWER, timestep_units='d', solver= 'cram48')

integrator.integrate()