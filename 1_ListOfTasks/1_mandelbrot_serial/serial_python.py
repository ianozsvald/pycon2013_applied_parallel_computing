"""Doesn't dereference on each iteration, goes faster!"""
import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D  # necessary magic import for 3D support

# area of space to investigate
x1, x2, y1, y2 = -2.13, 0.77, -1.3, 1.3

# plot in 2D for a fast output or 3D for a slower but prettier output
SHOW_IN_3D = False


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


#def show_2D_PIL(output):
    #"""Convert list to numpy array, show using PIL"""
    #try:
        #import Image
        ## convert our output to PIL-compatible input
        #import array
        ## scale the output to a 0..255 range for plotting
        #max_val = max(output)
        #output = [int(float(o) / max_val * 255) for o in output]
        #output = ((o + (256 * o) + (256 ** 2) * o) * 8 for o in output)
        #output = array.array('I', output)
        ## display with PIL
        #im = Image.new("RGB", (w / 2, h / 2))
        #im.fromstring(output.tostring(), "raw", "RGBX", 0, -1)
        #im.show()
    #except ImportError as err:
        ## Bail gracefully if we don't have PIL
        #print "Couldn't import Image:", str(err)


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


def calculate_z(q, maxiter):
    """Pure python with complex datatype, iterating over list of q and z"""
    output = [0] * len(q)
    for i in range(len(q)):
        zi = 0 + 0j
        qi = q[i]
        if i % 1000 == 0:
            # print out some progress info since it is so slow...
            print "%0.2f%% complete" % (1.0 / len(q) * i * 100)

        output[i] = maxiter  # force max value if we exceed maxiter

        for iteration in range(maxiter):
            zi = zi * zi + qi
            if abs(zi) > 2.0:
                output[i] = iteration
                break
    return output


def calc_pure_python(show_output):
    # make a list of x and y values which will represent q
    # xx and yy are the co-ordinates, for the default configuration they'll look like:
    # if we have a 1000x1000 plot
    # xx = [-2.13, -2.1242, -2.1184000000000003, ..., 0.7526000000000064, 0.7584000000000064, 0.7642000000000064]
    # yy = [1.3, 1.2948, 1.2895999999999999, ..., -1.2844000000000058, -1.2896000000000059, -1.294800000000006]
    x_step = (float(x2 - x1) / float(w)) * 2
    y_step = (float(y1 - y2) / float(h)) * 2
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step
    q = []
    for ycoord in y:
        for xcoord in x:
            q.append(complex(xcoord, ycoord))

    print "Total elements:", len(q)
    start_time = datetime.datetime.now()
    output = calculate_z(q, maxiter)
    end_time = datetime.datetime.now()
    secs = end_time - start_time
    print "Main took", secs

    validation_sum = sum(output)
    print "Total sum of elements (for validation):", validation_sum

    if show_output:
        if SHOW_IN_3D:
            show_3D(output)
        else:
            show_2D(output)

    return validation_sum


if __name__ == "__main__":
    # get width, height and max iterations from cmd line
    # 'python serial_python.py 1000 1000'
    if len(sys.argv) == 1:
        w = h = 1000
        maxiter = 1000
    else:
        w = int(sys.argv[1])
        h = int(sys.argv[1])
        maxiter = int(sys.argv[2])

    # we can show_output for Python, not for PyPy
    validation_sum = calc_pure_python(True)

    # confirm validation output for our known test case
    # we do this because we've seen some odd behaviour due to subtle student
    # bugs
    if w == 1000 and h == 1000 and maxiter == 1000:
        assert validation_sum == 51214485  # if False then we have a bug
