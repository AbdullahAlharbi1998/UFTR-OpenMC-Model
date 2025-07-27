# UFTR-OpenMC-Model

## Overview

This repository contains a high-fidelity, benchmarked, and validated full-geometry OpenMC model of the University of Florida Training Reactor (UFTR). It is designed for use in research, education, and daily operations.

## About UFTR

The UFTR is a training and research reactor located at the University of Florida. Here are some key details about it:

- **Type**: Argonaut-type reactor
- **First Critical**: 1959
- **License**: 100 kW
- **Fuel**: U3Si2-Al plates with a U-235 enrichment of 19.70% by weight
- **Cladding**: Al6061
- **Fuel arrangement**:
  - 14 plates make up one assembly
  - 4 assemblies make up one box
  - The core consists of 6 boxes arranged in two parallel rows, each containing 3 boxes, with two blades in between boxes
- **Neutron Absorption**: Control blades tipped with cadmium are inserted between the boxes
- **Cooling and Moderation**: Water flows from the bottom to the top between the plates and inside the boxes, serving as both the coolant and the neutron moderator
- **Reflector**: The core is composed and surrounded by a graphite, serving as both moderatot and reflector

## Core Design

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



c:\OpenMC\UFTR\GitHub Repository\fresh_core\Figures\full geometry radial.png
c:\OpenMC\UFTR\GitHub Repository\march2025_core\figures\XY zoomed.png
c:\OpenMC\UFTR\GitHub Repository\fresh_core\Figures\full geometry axial.png
c:\OpenMC\UFTR\GitHub Repository\march2025_core\figures\XZ zoomed.png
c:\OpenMC\UFTR\GitHub Repository\march2025_core\figures\YZ.png


## Model Benchmarking and Validation

There are to version of the model, one for the frsh core of 2006, and one for the core of March 2025, taking depletion into account, both versions has been validated against both experimental data taken directly from operation and an established MCNP model using four complementary methods. These validation efforts target key physical and operational parameters of the reactor. The results show strong agreement with experimental and reported data, increasing confidence in the model's predictive capabilities.

### 1. Reactivity Parameter Comparison

Reactivity parameters computed by the model were compared to those reported in experimental documentation for both the fresh core and the operational core as of July 2022. These parameters include excess reactivity, shutdown margin, and control blade worths. The comparison tables below illustrate the model’s agreement with experimental benchmarks.

#### Table 1. Fresh Core Reactivity and Kinetics Parameters Comparison

| Parameter                              | OpenMC              | Experimental   | MCNP     | δ₁ (%)    | δ₂ (%)   |
|----------------------------------------|---------------------|----------------|----------|-----------|----------|
| Excess Reactivity (pcm)                | 609±11              | 600            | 539      | 1.5       | 12.99    |
| Shutdown Margin (pcm)                  | 3267±13             | 3290           | 3441     | -0.7      | -5.06    |
| Safety Blade 1 Worth (pcm)             | 1379±12             | 1400           | 1414     | -1.5      | -2.47    |
| Safety Blade 2 Worth (pcm)             | 1717±14             | 1730           | 1793     | -0.75     | -4.24    |
| Safety Blade 3 Worth (pcm)             | 1835±14             | 1900           | 1841     | -3.4      | -0.49    |
| Regulating Blade Worth (pcm)           | 780±13              | 760            | 733      | 2.63      | 6.41     |
| K_eff at Critical Position             | 1.00046±0.00006     | 1.00000        | –        | 0.046     | –        |
| Prompt Neutron Lifetime (Λ) (μs)       | 218.7               | –              | 202.8    | –         | 7.84     |
| Delayed Neutron Fraction (β_eff) (pcm) | 743±7               | 742±1          | 740      | 0.13      | 0.41     |

<sup>a</sup> δ₁ = ((OpenMC − Experimental) / Experimental) × 100  
<sup>b</sup> δ₂ = ((OpenMC − MCNP) / MCNP) × 100

#### Table 2. Reactivity and Kinetics Parameters Comparison at 70,648 kWh (July 2022)

| Parameter                              | OpenMC Estimation       | Measured      | Difference (%) |
|----------------------------------------|-------------------------|---------------|----------------|
| Excess Reactivity (pcm)                | 957±11                  | 929           | 3.0            |
| Shutdown Margin (pcm)                  | 2879±14                 | 2800          | 2.8            |
| Safety Blade 1 Worth (pcm)             | 1312±13                 | 1248          | 5.1            |
| Safety Blade 2 Worth (pcm)             | 1641±12                 | 1564          | 4.9            |
| Safety Blade 3 Worth (pcm)             | 1753±13                 | 1823          | -3.8           |
| Regulating Blade Worth (pcm)           | 883±11                  | 915           | -3.5           |
| K_eff at Critical Position             | 1.00138±0.00007         | 1.00000       | 0.138          |
| Delayed Neutron Fraction (β_eff) (pcm) | 717±8                   | 733±10        | -2.2           |

These comparisons show good agreement overall. However, due to discrepancies in the experimental data (arising from differences in measurement methodology and assumptions), further validation is still recommended for increased confidence.

### 4. Fuel Burnup and Isotopic Buildup Tracking

The model's predictions for U-235 depletion and Pu-239/Pu-241 buildup were compared to operator-reported estimates at three burnup levels. Results are presented below:

#### Table 3. Uranium and Plutonium Tracking Comparison at Different Burnup Steps

| Burnup (kWh) | U-235 Loss (%) (Model) | U-235 Loss (%) (Reported) | Difference (%) | Pu-239/241 Gain (%) (Model) | Pu-239/241 Gain (%) (Reported) | Difference (%) |
|--------------|------------------------|----------------------------|----------------|------------------------------|--------------------------------|----------------|
| 0            | 0.000                  | 0.000                      | 0.0            | 0.000                        | 0.000                          | 0.0            |
| 14,174       | 0.759                  | 0.768                      | -1.2           | 0.055                        | 0.050                          | 10.0           |
| 70,647       | 3.788                  | 3.825                      | -1.0           | 0.276                        | 0.248                          | 11.3           |
| 105,386      | 5.663                  | 5.706                      | -0.8           | 0.409                        | 0.370                          | 10.5           |

This comparison further supports the model's reliability in long-term isotopic evolution prediction. However, the higher discrepancy observed in Pu-239 buildup compared to U-235 depletion highlights a key limitation of the current depletion estimation approach. While U-235 burnup is relatively straightforward to model due to its direct fission consumption, Pu-239 accumulation involves a more complex chain of transmutation reactions, which are sensitive to neutron flux history and spectral variations. This suggests that the reduced accuracy observed in the current core, relative to the fresh core, is primarily driven by uncertainties in depletion modeling — especially in capturing plutonium production accurately.

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
