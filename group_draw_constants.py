# Boundary conditions for group draw of GIKC 2023
#NUMBER_OF_ROUNDS = 6
#HEATS_PER_ROUND = 6
#DRIVER_PER_HEAT = 20


# Ask for boundary conditions of group draw
NUMBER_OF_ROUNDS = int(input("Number of rounds during the preliminary heats: "))
HEATS_PER_ROUND = int(input("Number of heats per round: "))
DRIVER_PER_HEAT = int(input("Number of drivers per heat: "))
print("All right! That means you have a total of " + str(DRIVER_PER_HEAT * HEATS_PER_ROUND) + " drivers and a total of " + str(HEATS_PER_ROUND * NUMBER_OF_ROUNDS) + " preliminary races.")