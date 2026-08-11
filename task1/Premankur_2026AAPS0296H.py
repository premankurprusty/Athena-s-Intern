# Premankur Prusty
# 2026AAPS0296H


# I could use pandas for dealing with the CSV file but i wanted to just use the python std lib

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as anim

# This is just opening the CSV file and appending all the values to the lists
data = open('Depth Data.csv', 'r')
next(data)
depthValues = []
time = []
for line in data:
    x,y = line.strip().split(',')
    time.append(x)
    depthValues.append(y)


# Converting all the depth values from string to float point and handling errors
for idx in range (0,len(depthValues)):
    try:
        depthValues[idx] = float(depthValues[idx])
    except ValueError:
        if idx == 0:
            depthValues[idx] = float(depthValues[idx+1])
        elif idx == len(depthValues) - 1:
            depthValues[idx] = float(depthValues[idx-1])
        else:
            depthValues[idx] = (float(depthValues[idx-1]) + float(depthValues[idx+1]))/2


# Making a copy of raw data before filtering
rawValues = depthValues.copy()

# Using median to filter out spikes
for idx in range (1, len(depthValues)-1):
    value = sorted([depthValues[idx-1], depthValues[idx], depthValues[idx+1]])
    depthValues[idx] = value[1]

# using mean to smooth out the graph
for idx in range (1, len(depthValues)-1):
    value = (depthValues[idx-1] + depthValues[idx] + depthValues[idx+1])/3
    depthValues[idx] = value

# plotting
fig, ax = plt.subplots(figsize=(14, 7))

# setting limits of the axes
ax.set_xlim(0, len(rawValues))
ax.set_ylim(min(rawValues + depthValues), max(rawValues + depthValues))

# creating both the lines
raw_line, = ax.plot([], [], alpha=0.35, label="Raw")
filtered_line, = ax.plot([], [], linewidth=2, label="Filtered")

# labeling
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Depth")
ax.set_title("Raw vs Filtered Depth")
ax.grid(True, alpha=0.25)
ax.legend()

# animating
def update(frame):
    x = range(frame + 1)

    raw_line.set_data(x, rawValues[:frame + 1])
    filtered_line.set_data(x, depthValues[:frame + 1])

    return raw_line, filtered_line

animation = anim(
    fig,
    update,
    frames=len(rawValues),
    interval=0,
    repeat=False
)

plt.show()
