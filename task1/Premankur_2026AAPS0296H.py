# Importing relevant libraries.
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as anim

# creating the plot and axes.
(fig,ax) = plt.subplots(figsize=(14, 7))

# creating the lines.
rawLine, = ax.plot([], [], alpha = 0.35, label = "Raw")
filteredLine, = ax.plot([], [], linewidth = 2, label = "Filtered")

# labeling the axes and graph.
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Depth")
ax.set_title("Depth vs Time Graph")
ax.grid(True, alpha = 0.1)
ax.legend()

# reading data.
data = open('Depth Data.csv', 'r')

#defining functions.
def median(a,b,c):
    values = sorted([a,b,c])
    return values[1]

# skipping the first line (Point,Depth (m)).
next(data)

# making the lists.
rawData = []
filteredData = []

# i'm using a variable named 'idx' because i'm assuming the number of data points won't be known beforehand, hence we cannot use a for loop (for idx in range (0,301)).
idx = 0


#this is my processing logic.
def update(frame):
    global idx
    line = next(data)
    (_,y) = line.strip().split(',')

    # tries to convert to float and just uses the previous depth in case of error.
    try:
        rawDepth = float(y)
    except ValueError:
        rawDepth = rawData[idx-1]

    rawData.append(rawDepth)

    # this 'margin' I use to remove spikes.
    margin = 30

    # it assumes that first two datapoints don't need checking and uses stores them directly.
    # I use the slope calculated by the previous two data-points to calculate a slope and make a prediction.
    # if the incoming value is past a margin of error, it is rejected and in place of it, the maximum (or minimum) allowed value is pushed and displayed on the graph.
    # based off some trial and error, a margin of 30-45 seems good, i decided to go with 30.
    if idx < 2:
        depth = rawDepth
    else:
        slope = filteredData[idx-1] - filteredData[idx-2]
        expectedDepth = filteredData[idx-1] + slope
        if (rawDepth - expectedDepth) > margin:
            depth = ((expectedDepth + margin)+filteredData[idx-1])/2
        elif (rawDepth - expectedDepth) < -margin:
            depth = ((expectedDepth - margin)+filteredData[idx-1])/2
        else:
            depth = rawDepth

    filteredData.append(depth)

    idx += 1

    # refreshes the lines and the axes and scaling of the graph.
    rawLine.set_data(range(len(rawData)), rawData)
    filteredLine.set_data(range(len(filteredData)), filteredData)

    ax.relim()
    ax.autoscale_view()

    return rawLine, filteredLine

# the animation.
animation = anim(
        fig,
        update,
        interval = 1000,
        repeat = False,
        cache_frame_data = False
        )

# displays the graph.
plt.show()
