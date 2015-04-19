import numpy as np
import itertools
import time

# function to print the Matrix in a zig zag format
def zig_zag_rect(matrix):
	start_time = time.time()

	# get the diagonals and then reverse the odd one's.
	diags = [matrix[::-1,:].diagonal(i) for i in range(-matrix.shape[0] + 1, matrix.shape[1])]
	diags = [j[::-1] if (i % 2 != 0) else j for i, j in enumerate(diags)]
	
	print("--- %s seconds ---" % (time.time() - start_time))
	
	# print "ZIG ZAG OUTPUT -> "
	print list(itertools.chain(*diags))
	print "----------------------------------"

# main function
def main():
	print "|-----------------------------------------------------|"
	print "| Testing a Square Matric (4 X 4)                     |"
	print "|-----------------------------------------------------|"
	row = 4
	col = 4
	A = np.random.randint(1000, size = (row, col))
	print A
	print "----------------------------------"
	zig_zag_rect(A)
	print "|-----------------------------------------------------|"
	print "| Testing Matric (3 X 4)                              |"
	print "|-----------------------------------------------------|"
	row = 3
	col = 4
	A = np.random.randint(1000, size = (row, col))
	print A
	print "----------------------------------"
	zig_zag_rect(A)
	print "|-----------------------------------------------------|"
	print "| Testing Matric (4 X 3)                              |"
	print "|-----------------------------------------------------|"
	row = 4
	col = 3
	A = np.random.randint(1000, size = (row, col))
	print A
	print "----------------------------------"
	zig_zag_rect(A)
	print "|-----------------------------------------------------|"
	print "| Testing Matric (3 X 2)                              |"
	print "|-----------------------------------------------------|"
	row = 3
	col = 2
	A = np.random.randint(1000, size = (row, col))
	print A
	print "----------------------------------"
	zig_zag_rect(A)

if __name__ == '__main__':
	main()