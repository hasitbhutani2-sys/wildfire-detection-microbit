import random
import time
import csv#for reading microbit csv data
 
density = 0.5#initial chance of a cell being a tree
growth = 0.5
temperature = 0.9#initial chance fire spreads
size = 10#forest size
steps=10#number of simulation steps

def load_data(file):#function to load csv data
    print("Loading file", file)
    with open(file) as f:
        reader=csv.reader(f)
        next(reader)#skip header row
        data=[list(map(float,row)) for row in reader]#convert all reamaining rows to float numbers
    temps=[row[1] for row in data]#temp=2nd column
    moist=[row[2] for row in data]#moisture=3rdcolumn
    #normalizes both lists to 0-1 scale for model usage
    temps=[t/max(temps) for t in temps]
    moist=[m/max(moist)for m in moist]
    return temps,moist
#load temperature and soil moisture data from csv file
#load csv file
#temp_data,moist_data=load_data("microbit.csv")
temp_data,moist_data=load_data("microbitdatawetsoil.csv")
 
forest = [['🟫' for i in range(size)] for j in range(size)]
 #populate initial trees randomnly based on density
for i in range(1,size-1):
    for j in range(1,size-1):
        if random.random()<density:
            forest[i][j] = '🌳'
#function to print forest 
def printForest():
    for row in forest[1:-1]:
        print(*row[1:-1])
    print()
 #tree growth function
def grow():
    #trees can grow into empty spaces and growth probability depends on soil moisture
    #'T' indiactes a new tree that becomes '🌳' in the next step 
    new=[row[:] for row in forest]
    for i in range(1,size-1):
        for j in range(1,size-1):
            if forest[i][j] == '🌳':
                if forest[i+1][j] == '🟫' and random.random()<growth:
                    new[i+1][j] = 'T'
                if forest[i][j+1] == '🟫' and random.random()<growth:
                    new[i][j+1] = 'T'
                if forest[i-1][j] == '🟫' and random.random()<growth:
                    new[i-1][j] = '🌳'
                if forest[i][j-1] == '🟫' and random.random()<growth:
                    new[i][j-1] = '🌳'
            if forest[i][j] == 'T':
                forest[i][j] = '🌳'
    forest[:]=new
#start fire function
def startFire():
    #randomnly selects a tree in the forest to ignite 
    while True:
        i=random.randint(1,size-2)
        j=random.randint(1,size-2)
        if forest[i][j]=='🌳':
            forest[i][j]='🔥'
            break
#burn function 
def burn():
    #spread fire from burning trees to trees'🌳'
    #fire spread probability depends on temperature and also returns the vount of burning trees in this step
    new=[row[:] for row in forest]
    #burning_count=0
    for i in range(1,size-1):
        for j in range(1,size-1):
            if forest[i][j] == '🔥':
                if forest[i+1][j] == '🌳' and random.random()<temperature:
                    new[i+1][j] = 'F'
                if forest[i][j+1] == '🌳' and random.random()<temperature:
                    new[i][j+1] = 'F'
                if forest[i-1][j] == '🌳' and random.random()<temperature:
                    new[i-1][j] = '🔥'
                if forest[i][j-1] == '🌳' and random.random()<temperature:
                    new[i][j-1] = '🔥'
 
    forest[:]=new
    #count number of currently burning trees
    burning_count=0
    for row in forest:
        burning_count+=row.count('🔥')
    return burning_count
 #SIMULATION LOOP
total_burned=0
for step in range(min(steps,len(temp_data))):
    temperature=temp_data[step]#Hotter=fire spreads more
    growth=0.2*moist_data[step]#wetter soil=trees regrow faster
#for step in range(steps):
    print("step:",step)#displays forest
    printForest()
    #start a new fire if there are no burning trees
    if all('🔥'not in row for row in forest):
        startFire()
        #spread fire
    burning=burn()
    total_burned+=burning
    #display fire info
    print("burning trees this step:",burning)
    print("Total burned so far:",total_burned)
    print("----------------------")
    #grow trees
    grow()
    #slows down the rate of the output
    time.sleep(0.3)    