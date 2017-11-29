def fib(levels):
	result = []
	for level in range(levels+1):	
		row = []
		for index in range(level):
			if index in (0, level-1):
				row.append(1)
			else:
				row.append(sum(result[-1][index-1:index+1]))
		result.append(row)
	return result[1:]


def plot_fib(levels, padding=0):
	if levels == []: return ''
	max_char = max([len(str(n)) for n in max(levels, key=max)]) + padding
	formatted_levels = [' '.join(['{num: ^{fill}}'.format(num=num, fill=max_char) for num in level]) for level in levels]
	max_len = len(formatted_levels[-1])
	return '\n'.join(['{num: ^{pad}}'.format(num=num, pad=max_len) for num in formatted_levels])


if __name__ == '__main__':
	result = fib(10)
	triangle = plot_fib(result)
	with open('result.txt', 'w') as f:
		f.write(triangle)
		print(triangle)