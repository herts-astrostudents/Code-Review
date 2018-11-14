import matplotlib.pyplot as plt


class ColourColourDiagram(object):
    """
    A matplotlib axes object with labels and a method to plot spectra
    """
    def __init__(self, xcolour, ycolour):
        self.figure, self.axes = plt.subplots()
        self.xcolour = xcolour
        self.ycolour = ycolour

        self.axes.set_xlabel(str(xcolour))  # we've used str(xcolour) to get the string representation of the colour 
        self.axes.set_ylabel(str(ycolour))


    def plot_table(self, table, **scatter_kwargs):
        xcolour = table[self.xcolour.filters[0].name] - table[self.xcolour.filters[1].name]
        ycolour = table[self.ycolour.filters[0].name] - table[self.ycolour.filters[1].name]
        self.axes.scatter(xcolour, ycolour, **scatter_kwargs)


    def plot_spectrum(self, spectrum, **scatter_kwargs):
        x = self.xcolour(spectrum)
        y = self.ycolour(spectrum)
        self.axes.scatter(x, y, **scatter_kwargs)


    def __repr__(self):
        """Always define __repr__ for you objects, it allows you to `print(my_object)`"""
        return "<ColourColourDiagram {} against {}>".format(self.axes.get_ylabel(), self.axes.get_xlabel())