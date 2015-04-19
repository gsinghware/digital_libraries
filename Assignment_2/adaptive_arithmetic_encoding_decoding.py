import random

# simple arithmetic encoding and decoding algorithn

def encode(string, probabilities):
	lower_bound = 0
	upper_bound = 1

	for symbol in string:
		symbol_lower_bound = probabilities[symbol][0]
		symbol_upper_bound = probabilities[symbol][1]
		# print symbol_lower_bound, symbol_upper_bound
		lower_bound = lower_bound + (symbol_lower_bound * upper_bound)
		upper_bound = upper_bound * symbol_upper_bound

	# print lower_bound, upper_bound
	return random.uniform(lower_bound, lower_bound+upper_bound)

def decode(decimal_number, probabilities):
	string = ""
	while True:
		for symbol in probabilities:
			symbol_lower_bound = probabilities[symbol][0]
			symbol_upper_bound = probabilities[symbol][1]
			if (0 <= decimal_number - symbol_lower_bound < symbol_upper_bound):
				string += symbol
				decimal_number = (decimal_number - symbol_lower_bound)/(symbol_upper_bound)
				print decimal_number, symbol
				break

		if (symbol == '@'):
			break

def main ():
	prob = {
		'a': [0, 0.4],
		'b': [0.4, 0.3],
		'c': [0.7, 0.2],
		'@': [0.9, 1]
	}

	print 'aababcbcacb@'
	encoded = encode('aababcbcacb@', prob)
	print encoded
	decoded = decode(encoded, prob)
	# print decoded

if __name__ == '__main__':
	main()













