import openmc as mc
import openmc.deplete
from fresh_core.fresh_core import fresh_core_model

print(fresh_core_model.materials)

mc.config['cross_sections'] = '/home/eastdusty/openmc_env/share/data/endfb80/endfb-viii.0-hdf5/cross_sections.xml'
# The cross-sections library used in this model was ENDF/B-VIII.0
# It can be downloaded using this link: https://openmc.org/official-data-libraries/

op = mc.deplete.CoupledOperator(fresh_core_model,'/home/eastdusty/openmc_env/share/data/endfb80/endfb-viii.0-hdf5/chain_endfb80_pwr.xml')
# this has to be a unique library for depletion analysis
# ENDF has one that can be found here: https://openmc.org/depletion-chains/, look for ENDF/B-VIII.0 Chain (Thermal Spectrum)

TIME = [608, 2311, 2648] # days
POWER = [969.6, 0, 888.7] # Watts

integrator = openmc.deplete.EPCRK4Integrator(op, timesteps=TIME, power=POWER, timestep_units='d', solver= 'cram48')

integrator.integrate()
