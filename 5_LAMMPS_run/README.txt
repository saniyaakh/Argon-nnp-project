neural network potential simulation files
=========================================

contents:
- lammps_1000_steps.lmp: input script for 1000 step simulation
- lammps_5000_steps.lmp: input script for 5000 step simulation
- plot_msd_pdf_1000steps.py: plotting script for msd and pdf
- plot_rdf_5000steps.py: plotting script for rdf
- neural network files (input.nn, scaling.data, weights.001.data)

usage:
run lammps simulation with: ./lmp -in lammps_xxxx_steps.lmp
analyze trajectory with: python3 ase_pp.py trajectory_file.atom
plot results with: python3 plot_script.py

note on simulation length:
the simulations used 1000-5000 steps due to limited disk storage space.
for better statistical quality and smoother rdf curves, increase the 
run steps to 10000 or higher in the lammps input files.
longer simulations provide better averaged results but require more
storage space and computation time.

neural network extrapolation warnings are normal and indicate the 
simulation is exploring configurations slightly outside the training data.
