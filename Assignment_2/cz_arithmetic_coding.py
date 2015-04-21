import random

def encode(string, prob):

	lower_bound = 0
	upper_bound = 1

	for symbol in string:
		curr_range = upper_bound - lower_bound

		upper_bound = lower_bound + (curr_range * prob[symbol][1])
		lower_bound = lower_bound + (curr_range * prob[symbol][0])

	return random.uniform(lower_bound, upper_bound)

def decode(encoded_num, prob):

	encoded_val = encoded_num

	while(not(0.9 <= encoded_val < 1)):
		for symbol in prob:

			if (prob[symbol][0] <= encoded_val < prob[symbol][1]):
				sym_lower = prob[symbol][0]
				sym_upper = prob[symbol][1]

				decoded_sym = symbol

				print encoded_val, decoded_sym

				if (symbol != '@'):
					curr_range = sym_upper - sym_lower
					encoded_val = (encoded_val - sym_lower) / curr_range



	



def main ():

	prob = {
		'a': [0, 0.4],
		'b': [0.4, 0.5],
		'c': [0.5, 0.9],
		'@': [0.9, 1]        # The character @ here is the EOF symbol.
	}

	encoded= encode('abcc@', prob)

	print encoded
	
	decode(encoded, prob)





if __name__ == '__main__':
	main()

