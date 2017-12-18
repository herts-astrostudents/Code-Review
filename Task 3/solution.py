#!/usr/bin/env python

def fib(nlevels):
    result = []
    for level in range(nlevels):
        row = [1]
        for index in range(1, level):
            row.append(sum(result[-1][index - 1:index + 1]))
        if level > 0:
            row.append(1)
        result.append(row)
    return result


def plot_fib(levels):
    if levels == []:
        return ''
    max_char = len(str(levels[-1][len(levels) // 2]))  # middle of last row
    formatted_levels = [' '.join(['{num: ^{fill}}'.format(num=num, fill=max_char) for num in level]) for level in
                        levels]
    max_len = len(formatted_levels[-1])  # string length of the last row
    return '\n'.join(['{level: ^{pad}}'.format(level=level, pad=max_len) for level in formatted_levels])


if __name__ == '__main__':
    # run with `python solution.py 10`
    import argparse

    parser = argparse.ArgumentParser(description='Prints the Fibonacci pyramid to stdout')
    parser.add_argument('nlevels', type=int)
    args = parser.parse_args()

    result = fib(args.nlevels)
    triangle = plot_fib(result)
    print(triangle)
