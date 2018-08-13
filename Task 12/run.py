from overlaps import overlap_python, overlap_numpy, overlap_pandas
import time


def measure_execution_time(function, args, iterations=100):
    '''
    Measure execution time of a function.

    function:   the function to be executed.
    args:       array of the arguments to pass to the function.
    iterations: how many times to run the function.

    Returns <float>: average execution time in ms.
    '''
    start_time = time.time()
    for i in range(iterations):
        function(*args)
    
    return 1000 * (time.time() - start_time) / iterations


primefile = 'primenumbers.txt'
happyfile = 'happynumbers.txt'

print( "overlap_python() executed in\t{} ms".format(
    measure_execution_time(
        overlap_python, [primefile, happyfile]
        )
    )
)

print( "overlap_numpy()  executed in\t{} ms".format(
    measure_execution_time(
        overlap_numpy, [primefile, happyfile]
        )
    )
)

print( "overlap_pandas() executed in\t{} ms".format(
    measure_execution_time(
        overlap_pandas, [primefile, happyfile]
        )
    )
)