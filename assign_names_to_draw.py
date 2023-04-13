import pickle
from pdf_helpers import create_race_pdf, create_personal_schedule

def get_anonymous_driver_list(races):
    anonym_driver_names_tmp = [list(races[1][heat]['driver'].keys()) for heat in range(1,NUMBER_OF_ROUNDS + 1)]
    anonym_driver_names = [item for sublist in anonym_driver_names_tmp for item in sublist]
    return sorted(anonym_driver_names)

def get_real_driver_list(filename):
    with open(filename, encoding='utf-8') as file:
        real_driver_names = [line.rstrip() for line in file]        
    return real_driver_names

def assign_driver_IDs(anonym_driver_names, real_driver_names):
    driver_ID_list = {}
    for i in range(len(anonym_driver_names)):
        driver_ID_list[anonym_driver_names[i]] = real_driver_names[i]  
    return driver_ID_list


def assign_names_to_race_overview(races, driver_ID_list):
    for round in races:
        for heat in races[round]:
            for driver in list(races[round][heat]['driver'].keys()):
                races[round][heat]['driver'][driver_ID_list[driver]] = races[round][heat]['driver'].pop(driver)
    return races

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

# Load group draw
with open('output/python-files/group-draw.pkl', 'rb') as file:      
    races = pickle.load(file)  

# Get boundary conditions of group draw
NUMBER_OF_ROUNDS = len(races)
HEATS_PER_ROUND = len(races[1])
DRIVER_PER_HEAT = len(races[1][1]['driver'])


# Get anonymous driver list
anonym_driver_names = get_anonymous_driver_list(races)

# Get driver list with real names
real_driver_names = get_real_driver_list("resources/entry_list.txt")

# Assign each driver to his Driver ID
driver_ID_list = assign_driver_IDs(anonym_driver_names, real_driver_names)

# Save the driver_ID_list in a file
with open('output/python-files/driver_IDs.pkl', 'wb') as file:
    pickle.dump(driver_ID_list, file)

# Replace anonymous names with true names
races = assign_names_to_race_overview(races, driver_ID_list)

# Create Heat PDFs
print("Creating Race PDFs...")
for round in range(1,NUMBER_OF_ROUNDS+1):
    for heat in range(1, HEATS_PER_ROUND+1):
        create_race_pdf(races, round, heat, DRIVER_PER_HEAT)

# Create personal driver schedule
print("Creating Personal Race Schedules...")
for driver in real_driver_names:
    # Ged driver's data
    data = get_drivers_races(driver, races)
    create_personal_schedule(data, driver, races, NUMBER_OF_ROUNDS, HEATS_PER_ROUND, DRIVER_PER_HEAT)

print("Done!")
    

