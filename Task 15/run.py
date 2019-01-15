from field_generator import generate_map
from bayfordbury_load import download_all
from plotter import plot_psf
from solution import estimate_psf
import matplotlib.pyplot as plt


def get_images(real=False):
    if real:
        return download_all("bayfordbury_ids.txt")

    # generate two images, one with a narrow PSF, one with a wide one
    widths = [1, 12] 
    return [("sigma_{}".format(width), generate_map(
            shape=(400, 400), nstars=50, noise=0.6,
            real_stars=True, max_width=width, seed=10)) for width in widths]


if __name__ == '__main__':
    real_images = True

    print("Gettings images...")
    images = get_images(real=real_images)
    
    print("Measuring PSFs...")
    psfs = [(image[0], estimate_psf(image[1], nstars=30, size=25)) for image in images]

    print("Plotting...")
    for i in range(len(images)):
        plot_psf(images[i], psfs[i], colormap="viridis")

    plt.show()