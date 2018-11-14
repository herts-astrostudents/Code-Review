from astropy.io import fits
from astropy import units as u


class Spectrum(object):
    def __init__(self, wavelengths, flux_density_wavelength):
        self.wavelengths = wavelengths
        self.flux_density_wavelength = flux_density_wavelength


    @classmethod
    def from_file(self, filename):
        """
        A classmethod is a type of function in a class which does not require that you have instantiated it. For example:
        >>> spectrum = Spectrum.from_file('spec-1954.fits')
        These methods are usually used as just a sneaky way of calling __init__ in a particular way. 
        In normal methods, the first argument is `self` (the object itself), whereas in classmethods, the first argument is the class.
        """
        hdus = fits.open(filename)
        data = hdus[1].data
        flux_density_wavelength = data['flux'] * 1e-17 * u.erg/u.s/u.cm/u.cm/u.Angstrom
        wavelengths = (10**data['loglam']) * u.Angstrom
        
        # Make a Spectrum object and return it!

        raise NotImplementedError("You need to return a `Spectrum` object here!")


    def __repr__(self):
        """Always define __repr__ for you objects, it allows you to `print(my_object)`"""
        return "<{}>".format(self.__name__)