"""Doesn't dereference on each iteration, goes faster!"""
import multiprocessing
import argparse
import datetime
import plotting

# Usage:
# $ python serial_python.py -s 300 -m 100 --plot3D
# by default it will use a size of 1000, max iterations 1000, 2D plotting
# we can use a size of 300 and max iterations 100 to iteratively test new code
# note that a 3D plot is quite slow

# area of space to investigate
x1, x2, y1, y2 = -2.13, 0.77, -1.3, 1.3

# plot in 2D for a fast output or 3D for a slower but prettier output
SHOW_IN_3D = False


def calculate_z((q, maxiter)):
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

    # split work list into continguous chunks, one per CPU
    # build this into chunks which we'll apply to map_async
    nbr_chunks = 128  # experiment with different nbrs of chunks
    #nbr_chunks = multiprocessing.cpu_count()
    print "Multiprocessing using {} CPUs".format(nbr_chunks)
    chunk_size = len(q) / nbr_chunks

    # split our long work list into smaller chunks
    # make sure we handle the edge case where nbr_chunks doesn't evenly fit into len(q)
    if len(q) % nbr_chunks != 0:
        # make sure we get the last few items of data when we have
        # an odd size to chunks (e.g. len(q) == 100 and nbr_chunks == 3
        nbr_chunks += 1
    chunks = [(q[x * chunk_size:(x + 1) * chunk_size], maxiter) for x in xrange(nbr_chunks)]
    print chunk_size, len(chunks), len(chunks[0][0])

    # create a Pool which will create Python processes
    p = multiprocessing.Pool()
    start_time = datetime.datetime.now()
    # send out the work chunks to the Pool
    # po is a multiprocessing.pool.MapResult
    po = p.map_async(calculate_z, chunks)
    # we get a list of lists back, one per chunk, so we have to
    # flatten them back together
    # po.get() will block until results are ready and then
    # return a list of lists of results
    results = po.get()  # [[ints...], [ints...], []]
    output = []
    for res in results:
        output += res
    end_time = datetime.datetime.now()
    secs = end_time - start_time

    print "Main took", secs

    validation_sum = sum(output)
    print "Total sum of elements (for validation):", validation_sum

    if show_output:
        if SHOW_IN_3D:
            plotting.show_3D(output)
        else:
            plotting.show_2D(output)

    return validation_sum


if __name__ == "__main__":
    # get width, height and max iterations from cmd line
    # 'python serial_python.py 1000 1000'
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('--size', '-s', type=int, help='Range for our width and height (e.g. 1000)', default=1000)
    parser.add_argument('--maxiterations', '-m', type=int, help='Maximum number of iterations (e.g. 1000)', default=1000)
    parser.add_argument('--plot3D', action="store_true", help='Plot in 3D (default is 2D)', default=False)
    args = parser.parse_args()
    print args
    w = h = args.size
    maxiter = args.maxiterations
    if args.plot3D:
        SHOW_IN_3D = True
    print "Using a width and height of {} and a maximum of {} iterations".format(w, maxiter)

    # we can show_output for Python, not for PyPy
    validation_sum = calc_pure_python(True)

    # confirm validation output for our known test case
    # we do this because we've seen some odd behaviour due to subtle student
    # bugs
    if w == 1000 and h == 1000 and maxiter == 1000:
        assert validation_sum == 51214485  # if False then we have a bug
