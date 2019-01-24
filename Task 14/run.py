import matplotlib.pyplot as plt

from solution import read_data, plot_temperature_map

dataset = read_data('data')
plot_temperature_map(dataset, month=1)  # plot the temperature over x and y coordinates in February with an optional colourmap
plot_temperature_map(dataset, month=8, cmap='viridis')
plt.show()