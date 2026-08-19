# Task 1:
My first approach for this project was to take the entire CSV file and process it and then produce an animated graph out of it. I later realized that the problem asked for the data to be processed as if it was being produced in real time, hence i decided to iterate over the dataset one by one and only use currently available data and previously known data to filter out some noise and the spikes. I did this by defining a margin of error and predicting a point off of the previous two points, if the incoming data was outside given 'margin of error' it is replaced by the mean of the max/min possible value (prediction +- margin) and the previous value. then i updated the graph in real time using matplotlib's features.

# Task 2:
I approached this by basically just opening Tinkercad, asking ChatGPT how Arduinos work and then learning enough c++ to make this.
I created an enum of possible types and an anchor boolean.
I first setup current state as opensea and then made a loop that runs forever.
The loop checks for readings and also button presses
If button is pressed then the anchor boolean is flipped
If anchor is dropped then no other checks go through because in every case of the switch statement, the first check is if anchor is dropped or not.
IF certain criteria is met and the state changes, then a function is called which updates the LCD display.
If ship is wrecked then state cannot be changed anymore.
