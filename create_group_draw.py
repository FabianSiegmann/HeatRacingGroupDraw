import random
import pickle

from group_draw_constants import NUMBER_OF_ROUNDS, HEATS_PER_ROUND, DRIVER_PER_HEAT
from group_draw_genetic_solver import GeneticSolver
from pdf_helpers import create_race_pdf, create_personal_schedule

def get_start_times(filename):
    with open(filename, encoding='utf-8') as file:
        start_times = [line.rstrip() for line in file]
    return start_times

def create_race_overview(new_groups, start_times):
    kart = 0
    races = {}
    for round in range(1,NUMBER_OF_ROUNDS+1):
        races[round] = {}
        for heat in range(1,HEATS_PER_ROUND+1):
            races[round][heat] = {"name": "Round " + str(round) + " - Heat " + str(heat), "time": start_times[(round-1)*NUMBER_OF_ROUNDS+heat-1], "driver": {"Driver " + '{:03}'.format(driver + 1): kart for driver in new_groups[round-1]['groups'][heat-1] }}
    return races


def get_anonymous_driver_list(races):
    anonym_driver_names_tmp = [list(races[1][heat]['driver'].keys()) for heat in range(1,NUMBER_OF_ROUNDS + 1)]
    anonym_driver_names = [item for sublist in anonym_driver_names_tmp for item in sublist]
    return sorted(anonym_driver_names)

def shuffle_list(list):
    random.shuffle(list)
    return list

def check_for_duplicates(list):
    list = [i for i in list if i != 0]
    if len(list) == len(set(list)):
        return False
    else:
        return True   
    
def get_drivers_karts(driver):
    drivers_karts = {}
    for round in range(1,NUMBER_OF_ROUNDS+1):
        drivers_karts[round] = {}
        for heat in range(1,HEATS_PER_ROUND+1):
            if driver in races[round][heat]['driver']:
                drivers_karts[round]['kart'] = races[round][heat]['driver'][driver]
    drivers_kart_list = [entry['kart'] for entry in drivers_karts.values()]
    return drivers_kart_list

def kart_draw_okay(list):
    list = [i for i in list if i != 0]
    for driver in list:
        if check_for_duplicates(get_drivers_karts(driver)):
            return False
    return True

def assign_kart_draw(races, driver_names):
    for round in range(1,NUMBER_OF_ROUNDS+1):
        for heat in range(1,HEATS_PER_ROUND+1):
            while True:
                kart_index = 0
                kart_list = shuffle_list(list(range(1, DRIVER_PER_HEAT+1)))
                for driver in races[round][heat]['driver']:
                    kart_num = kart_list[kart_index]
                    races[round][heat]['driver'][driver] = kart_num
                    kart_index += 1
                if kart_draw_okay(driver_names):
                    break
    # Safety check: verify the whole kart draw
    if kart_draw_okay(driver_names):    
        return races
    else:
        raise Exception



def get_drivers_races(driver, races):
    drivers_races = {}
    for round in range(1,NUMBER_OF_ROUNDS+1):
        drivers_races[round] = {}
        for heat in range(1,HEATS_PER_ROUND+1):
            if driver in races[round][heat]['driver']:
                drivers_races[round]['race'] = races[round][heat]['name']
                drivers_races[round]['kart'] = races[round][heat]['driver'][driver]
                drivers_races[round]['time'] = races[round][heat]['time']
    return drivers_races




    


# Get anonymous group draw
print("Creating group draw...")
solver = GeneticSolver(
    numberOfGroups=HEATS_PER_ROUND, sizeOfGroups=DRIVER_PER_HEAT, numberOfRounds=NUMBER_OF_ROUNDS)
groups = solver.solve()
print("Group draw created successfully!")

# Get timing schedule
start_times = get_start_times("resources/timing.txt")

# Get race overview
races = create_race_overview(groups, start_times)

# Get anonymous driver list
anonym_driver_names = get_anonymous_driver_list(races)

# Perform random kart draw for each group and thereby make sure that no driver drives a kart more than once
print("Creating kart draw...")
races = assign_kart_draw(races, anonym_driver_names)
print("Kart draw created successfully!")

# Save group and kart draw in a file
with open('output/python-files/group-draw.pkl', 'wb') as file:
    pickle.dump(races, file)


# Create Heat PDFs
print("Creating Race PDFs...")
for round in range(1,NUMBER_OF_ROUNDS+1):
    for heat in range(1, HEATS_PER_ROUND+1):
        create_race_pdf(races, round, heat, DRIVER_PER_HEAT)

# Create personal driver schedule
print("Creating Personal Race Schedules...")
for driver in anonym_driver_names:
    # Ged driver's data
    data = get_drivers_races(driver, races)
    create_personal_schedule(data, driver, races, NUMBER_OF_ROUNDS, HEATS_PER_ROUND, DRIVER_PER_HEAT)

print("Done!")