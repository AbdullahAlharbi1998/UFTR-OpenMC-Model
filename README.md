# UFTR-OpenMC-Model

## Overview

This repository contains a high-fidelity, benchmarked, and validated full-geometry OpenMC model of the University of Florida Training Reactor (UFTR). It is designed for use in research, education, and daily operations.

Additionally, it contains various input automation, output processing, and other useful OpenMC scripts, making it a good example and demonstration for a real life application of OpenMC 

## Quick files guide

fresh_core.py and march2025_core.py are the main scripts, while the jupyter notebook versions of those serve as a demonstration and can be both executed and used, the rest are I/O and xml run setup files 

## About the UFTR reactor

- **Type**: Modified Argonaut-type reactor
- **First Criticality**: 1959
- **Most significant modification**: HEU to LEU fuel conversion in 2006
- **License**: 100 kW
- **Fuel**: U3Si2-Al plates with a U-235 enrichment of 19.70% by weight
- **Cladding**: Al6061
- **Fuel arrangement**:
  - 14 fuel plates/assembly
  - 4 fuel assemblies/box
  - 6 fuel boxes/core; the 6 boxes are arranged in two parallel rows, each containing 3 boxes, with two blades in between boxes
- **Neutron Absorption**: Control blades tipped with cadmium are inserted between the boxes
- **Cooling**: Water flows from the bottom to the top between the plates and inside the boxes
- **Moderation**: Both water and graphite contribute to the slowing down of neutrons, also both have very similar reactivity worths
- **Reflector**: The core is composed and surrounded by nuclear grade graphite strings, serving as both moderator and reflector

## geometry schematics

### Color Convention

| Material / Region           | Color   |
|----------------------------|---------|
| Old Fuel                   | Red     |
| New Fuel                   | Orange  |
| Water                      | Blue    |
| Aluminum                   | Silver  |
| Graphite                   | Grey    |
| Air                        | Black   |
| Magnesium Blade Casing     | Purple  |
| Cadmium (Control Material) | Green   |
| Concrete                   | Brown   |



![full geometry radial.png](fresh_core%2FFigures%2Ffull%20geometry%20radial.png)
![XY zoomed.png](march2025_core%2Ffigures%2FXY%20zoomed.png)
![full geometry axial.png](fresh_core%2FFigures%2Ffull%20geometry%20axial.png)
![XZ zoomed.png](march2025_core%2Ffigures%2FXZ%20zoomed.png)
![YZ.png](march2025_core%2Ffigures%2FYZ.png)


## Model Benchmarking and Validation

There are two versions of the model, one for the LEU fresh core of 2006, and one for the core of March 2025, both models are validated, although the fresh core version has slightly higher fidelity, the benchmarking parameters included the following:

1- Reactivity parameters

2- Criticality parameters

3- Neutron flux spectra

4- Neutron flux distribution

5- Power peaking factors (PPF)

6- Isotopic evolution and buildup

7- Internal diagnostics


below are some of the benchmarking results of the LEU fresh core of 2006 against an already validated MCNP model and reliable NRC-vetted experimental data that led to the validation conclusion:

### Table 1. Comparison of reactivity and kinetics parameters for OpenMC, MCNP, and experimental measurements

| **Parameter** | **Method** | **Method** | **Method** | **Deviation (pcm)** | **Deviation (pcm)** |
|---|---|---|---|---|---|
|  | **OpenMC** | **Experimental** | **MCNP** | **δ₁** | **δ₂** |
| Safety Blade 1 Worth (pcm) | 1378 ± 7 | 1400 | 1414 | −22 | −36 |
| Safety Blade 2 Worth (pcm) | 1783 ± 6 | 1730 | 1793 | 53 | −10 |
| Safety Blade 3 Worth (pcm) | 1828 ± 6 | 1900 | 1841 | −72 | −13 |
| Regulating Blade Worth (pcm) | 770 ± 7 | 760 | 733 | 10 | 37 |
| Prompt Neutron Lifetime (Λ) (μs) | 218.7 | – | 202.8 | – | – |
| Delayed Neutron Fraction (βₑff) (pcm) | 743 ± 7 | 742 ± 1 | 740 | 1 | 3 |

**Notes**  
- δ₁ = ρ(OpenMC) − ρ(Experimental)  
- δ₂ = ρ(OpenMC) − ρ(MCNP)

### Table 2. Comparison of criticality parameters for OpenMC, MCNP, and experimental measurements

| **Parameter** | **Method** | **Method** | **Method** | **Deviation (pcm)** | **Deviation (pcm)** |
|---|---|---|---|---|---|
|  | **OpenMC** | **Experimental** | **MCNP** | **δ₁** | **δ₂** |
| *K*ₑff at First Experimental CP | 1.00026 ± 0.00005 | 1.00000 | – | 26 | – |
| *K*ₑff at Second Experimental CP | 0.99928 ± 0.00005 | 1.00000 | – | −72 | – |
| *K*ₑff at Third Experimental CP | 1.00046 ± 0.00005 | 1.00000 | – | 46 | – |
| *K*ₑff at MCNP predicated CP | 1.00071 ± 0.00005 | – | 1.00000 | – | 71 |
| Excess Reactivity (pcm) | 605 ± 4 | 600 | 539 | 5 | 66 |
| Shutdown Margin (formal method)ᵃ (pcm) | 3368 ± 7 | – | 3441 | – | −73 |
| Shutdown Margin (experimental method)ᵇ (pcm) | 3326 ± 24 | 3290 | 3401 | 36 | −75 |

**Notes**  
ᵃ *formal method*: ρ when all blades are inserted while the blade with the highest reactivity worth is withdrawn.  
ᵇ *experimental method*: (sum of all blade worths except the one with the highest worth) − (excess reactivity).

## Areas for Improvement

While the model demonstrates strong agreement with experimental data, several enhancements are identified that could further improve its accuracy and extend its utility. These areas are listed below in order of significance.

### 1. Depletion Modeling and Operational History Representation

Results show a noticeable decline in predictive accuracy when comparing the fresh core to the current core. This is primarily attributed to simplifications in the depletion process. Such approximations are common in research reactor modeling, where long-term operational history is difficult to reconstruct due to the inherently stochastic and inconsistent nature of daily usage.

Most depletion approaches assume simplified irradiation steps at constant power over fixed durations — a methodology that is appropriate for commercial power reactors but poorly suited to the irregular operation of training and research reactors like UFTR. These simplifications introduce biases in isotopic evolution, affecting parameters like reactivity, blade worth, and β-effective in current core analyses.

Nevertheless, opportunities exist to improve depletion modeling by:
- Incorporating more granular irradiation schedules based on historical logs.
- Sensitivity analysis to bracket the impact of different operational histories.
- Exploring time-dependent burnup tools or coupling to external solvers.

Improving this aspect is considered the **most impactful path forward** for enhancing the model's accuracy.

### 2. Transition to CAD-Based Geometry

The current model uses Constructive Solid Geometry (CSG), which limits spatial fidelity for complex components. Transitioning to CAD-based geometry via DAGMC would allow for greater detail in core structures and experimental facilities. Tools such as Coreform Cubit are particularly well-suited for nuclear applications. A comparative study between CSG and CAD-based results would quantify potential gains in precision.

### 3. Refined Shielding Model

The surrounding concrete shielding is currently approximated. Notably, additional shielding was installed when the UFTR's licensed maximum power increased from 10 kW to 100 kW. More accurate modeling of this configuration would improve predictions of radiation leakage and better support safety and shielding evaluations.

### 4. Multiphysics Integration

The model currently focuses on neutron transport, but OpenMC’s compatibility with external frameworks such as MOOSE, COMSOL, and OpenFOAM opens the door for coupled multiphysics simulations. Integrating thermal-hydraulics and structural effects would allow for more realistic and holistic simulations — especially valuable for transient or feedback studies.

### 5. Improved Fuel Assembly Structural Details

Some geometric simplifications were made for aluminum screws, holders, and internal supports within the fuel assemblies. While minor in terms of global reactor physics, incorporating these components could improve local flux distributions and activation predictions, particularly for experiment planning or shielding assessments.

## Developers

- **Lead Developer**: Abdullah Alharbi  
- **Advisor**: Dr. Justin Watson  
- **Institution**: Developed at the University of Florida

## Usage

This model can be utilized for various purposes including educational demonstrations, operational planning, safety analyses, and research & experimentation.

## Contact

For inquiries, suggestions, collaboration requests, or feedback regarding this model or its applications, please contact:

- **Abdullah Alharbi**: amsh326@hotmail.com  
- **Dr. Justin Watson**: justin.watson@ufl.edu