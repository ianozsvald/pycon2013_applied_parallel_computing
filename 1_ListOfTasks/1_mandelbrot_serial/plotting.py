import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D  # necessary magic import for 3D support


def show_2D(output):
    """Plot quickly in 2D"""
    width = np.sqrt(len(output))
    Z = np.array(output).reshape((width, width))
    fig = plt.figure()
    fig.suptitle("Mandelbrot")

    # setup a colormap that emphasises the detail of a 1000 iteration
    # calculation
    scale = ((0.0, 0.0, 0.0),
             (0.01, 0.3, 0.3),
             (0.1, 0.9, 0.9),
             (1.0, 1.0, 1.0))
    cdict = {'red': scale, 'green': scale, 'blue': scale}
    my_cmap = colors.LinearSegmentedColormap('my_colormap', cdict, 256)
    # plot our matrix using the new colormap
    plt.imshow(Z, cmap=my_cmap, interpolation='nearest')
    plt.show()


def show_3D(output):
    """Show using matplotlib as 3D surface plot"""
    width = np.sqrt(len(output))
    Z = np.array(output).reshape((width, width))
    fig = plt.figure()
    fig.suptitle("Mandelbrot")

    """Plot far more slowly in 3D"""
    assert Axes3D.name == "3d"  # dummy test so pylint knows that Axes3D has usage
    Xr = np.arange(width)
    Yr = np.arange(width)
    X, Y = np.meshgrid(Xr, Yr)
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    cmap = 'jet'
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cmap, linewidth=0, antialiased=True, shade=True)
    plt.show()
