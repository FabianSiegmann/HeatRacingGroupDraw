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
Except for the latter, those modules should be included in any usual python installation. You can install the *fpdf* module in your command line via:
```
pip install fpdf
```

# Usage
When the requirements are fullfilled, the programm can be executed by running *create_group_draw.py* and specifying the boundary conditions of your group draw. The programm will ask for the following details:
```
Number of rounds during the preliminary heats
Number of heats per round
Number of drivers per heat
```
where the first one is not the total number of heats, but the number of heats that each driver will participate in.

The programm will than create a group and kart draw with anonymous names (Driver 001, Driver 002, etc). The results will be printed as PDF in the *output* folder. It will also store the draw in a pickle file that can be used afterwards. Therefore the program uses the *timing.txt* file from the *resources* folder. To use your own schedule you can replace this file with your own schedule (using the same formatting. First line of text file represents start time of first race, second line represents start time of second race, etc)

If you want to assign real driver names to your draw, you can do so by replacing the *entry_list.txt* in the *resources* folder with your actual driver names (again, using the same formatting: First line of text file represents "Driver 001", second line represents "Driver 002", etc.) and then run the file *assign_names_to_draw*.

This will replace the anonymous driver names with your real driver names. 

For GIKC 2023, the assignment between real driver names and anonymous driver names will be performed with a raffle. 

# Acknowledgements
The group draw in this project is based on previous work regarding the *Social-Golfer-Problem* from Brad Buchanan: https://github.com/islemaster/good-enough-golfers

