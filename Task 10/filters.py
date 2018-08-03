from astropy import units as u
from astropy.constants import c
from astropy.table import Table
from scipy.integrate import simps as simpsons_rule_integration
import numpy as np

def flux2ABMag(flux):
    """returns the AB magnitude of a flux"""
    return -2.5 * np.log10(flux.to(u.Jy).value) - 48.6


class Filter(object):
    """
    An object to hold the response of a filter curve with methods to act upon Spectrum objects
    """
    def __init__(self, wavelengths, response, name=None):
        # __init__ is how the object is setup. When you do `my_object = my_object_class()` the object is created from the object class (its definition)
        # and then __init__ is automatically called after that to do any setup which is needed. Here we just give it some data
        # It is common to `Spectrum` for a class name and `spectrum` for its object. So `spectrum = Spectrum(...)`
        self.wavelengths = wavelengths
        self.response = response
        self.name = name


    def propagate_ABmagnitude(self, spectrum):
        """
        Calculates the quantity:
        flux_density = integral(flux_density * response / wavelength, dwavelength) / integral(response / wavelength, dwavelength)
        over the filter's wavelength range
        This is the flux density you would see in using this filter when you look at the object that this spectrum is emitted from.
        """

        # 1. Interpolate the filter response to the spectrum wavelengths using np.interp
        # 2. Convert the spectrum flux to Janskys using the relation `wavelength * flux_density_wavelength = frequency * flux_density_frequency`
        # 3. Calculate the integrals above using simpsons rule to get the average flux density 
        # 4. Get the flux_density (in Janskys), with its unit (`*u.Jy`)
        # 5. Return the AB magnitude


        select = spectrum.wavelengths > self.wavelengths.min()
        select &= spectrum.wavelengths < self.wavelengths.max()
        flux_density_wavelength = spectrum.flux_density_wavelength[select]
        wavelength = spectrum.wavelengths[select]

        raise NotImplementedError("You need to get the `average_flux_density_jansky` that the spectrum would have in this filter. Look at the comments!")
        return flux2ABMag(average_flux_density_jansky)


    def __call__(self, spectrum):
        """
        A call to the filter object would logically mean propgate a spectrum 
        >>> my_spectrum = Spectrum(...)
        >>> my_filter = Filter(...)
        >>> my_mag = my_filter(my_spectrum)
        """
        return self.propagate_ABmagnitude(spectrum)


    def __sub__(self, other):
        """
        This is a python magic method, it allows this object to use the subtract `-` operator.
        E.g.
        >>> filter_u = Filter.from_file('u.fits')
        >>> filter_g = Filter.from_file('g.fits')
        >>> colour = filter_u - filter_g  # This gives us a `Colour` of `u - g`
        Since astronomical colours are magnitude differences we can say that one filter minus another is 
        equivalent to a colour
        So this method must return a colour
        """
        raise NotImplementedError("Subtracting a filter from a filter must return a Colour object!")


    def __repr__(self):
        """Always define __repr__ for you objects, it allows you to `print(my_object)`"""
        return "<Filter name={}>".format(self.name)


    @classmethod
    def from_file(cls, filename):
        """
        A classmethod is a type of function in a class which does not require that you have instantiated it. For example:
        >>> filter = Filter.from_file('sdss-i.fits')
        These methods are usually used as just a sneaky way of calling __init__ in a particular way. 
        In normal methods, the first argument is `self` (the object itself), whereas in classmethods, the first argument is the class.
        """
        t = Table.read(filename)
        return cls(t['wavelength'].data * t['wavelength'].unit, t['response'].data, name=t.meta['NAME'])



class Colour(object):
    """
    Makes a magnitude colour from Filter objects
    >>> filter1 = Filter.from_sdss('i')
    >>> filter2 = Filter.from_sdss('g')
    >>> colour = Colour(filter1, filter2)
    >>> magnitude_colour = colour(spectrum)  # give it a spectrum and it will give you the magnitude colour
    This is equivalent to the colour i - g
    """
    def __init__(self, filter1, filter2):
        self.filters = [filter1, filter2]


    def __call__(self, spectrum):
        mag1 = self.filters[0](spectrum)
        mag2 = self.filters[1](spectrum)
        return mag1 - mag2


    def __repr__(self):
        """
        Always define __repr__ for you objects, it allows you to `print(my_object)`
        """
        return "${} - {}$".format(self.filters[0].name, self.filters[1].name)
