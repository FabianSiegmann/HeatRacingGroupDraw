# HeatRacingGroupDraw
In this repository, we present a method that allocates a certain number of drivers into a certain number of groups over a certain number of rounds. 

The method is based on an initial randomly distributed group assignment, which is then optimized in a way that "multiple meetings" of the same competitors are minimized. 

Furthermore, each participant is assigned a kart number for each of his races. This assignment is also randomly based, but with the boundary condition that no driver can be assigned to a specific kart number more than once. That means that each driver will be assigned with a different kart for each round.

# Requirements
The code is written in python and uses the modules 
```
random
itertools
math
fpdf
```
Except for the latter, those modules should be included in any usual python installation. You can install the *fpdf* module ib your command line via:
```
pip install fpdf
```

# Usage
When the requirements are fullfilled, the programm can be executed by running *create_group_draw.py*

# Acknowledgements
