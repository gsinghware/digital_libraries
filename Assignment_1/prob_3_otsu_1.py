# Gurpreet Singh
# Digital Libraries
# Assignment 1, problem 3

##########################################################################################################################

# README
# main(): calls otsu_construct() with image input
# otsu_construct(): does all the work for global threshold, local threshold and overlapping
# otsu_threshold(): give hist and size of the image to compute a threshold

##########################################################################################################################

import cv2
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
from scipy import misc

# for testing purposes
from skimage.filters import threshold_otsu, rank


# Otsu's Thresholding Method: 
# Find the threshold that seperates the background from the foreground.
# Find the threshold that minimizes the weighted within-class variance.
# Find the threshold such the variance of the two gaussian is at minimum. 
# This turns out to be same as maximizing the between-class variance.
# Histogram of the image must be bimodal. (having two modes)

# Original otsu threshold
# otsu_threshold1(hist)
# hist is the histogram (256 bins) of the imag
# size if the size of the image (total pixels)
# returns a threshold for the img

##########################################################################################################################

def otsu_threshold(hist, size):
	# minimize within-class variance
	min_within_class_variance = 0
	min_within_class_variance_idx = 0

	for t in xrange(0, 256):
		# from 0 to threshold t
		# sum the probabilities

		# CLASS 1 in bi-modal histogram (Background)
		# qi = sigma(i = 0, t) p(i)
		qt1 = float(sum(hist[0:t]))							# sum of the frequencies
		qtz = qt1/size										# divide by size to get the probabilities

		mean_t1 = 0											# class 1 mean
		variance_t1 = 0	   									# class 1 variance
		if (qt1 > 0): 										# if the sum
			for i in range(0, t):							
				mean_t1 += (i * hist[i])
			mean_t1 = (mean_t1 / qt1)						# the ean of the 

			for i in range(0, t):
				variance_t1 += (((i - mean_t1)**2) * hist[i]) # variance
			variance_t1 = (variance_t1 / qt1)

		# # CLASS 2 in bi-modal histogram (Foreground)
		qt2 = float(sum(hist[t:256]))						# qi = sigma(i = t+1, 256) p(i) 
		qtl = qt2/size									# divide to get the probabilities
			
		mean_t2 = 0
		variance_t2 = 0
		if (qt2 > 0):
			for i in range(t, 256):
				mean_t2 += (i * hist[i])
			mean_t2 = (mean_t2 / qt2)

			for i in range(t, 256):
				variance_t2 += (((i - mean_t2)**2) * hist[i])
			variance_t2 = (variance_t2 / qt2)

		variance_w_t_sq = qtz * variance_t1 + qtl * variance_t2

		if (t == 0):
			min_within_class_variance = variance_w_t_sq
			min_within_class_variance_idx = t

		if (variance_w_t_sq < min_within_class_variance):
			min_within_class_variance = variance_w_t_sq
			min_within_class_variance_idx = t

	# minimize the within-class variance
	# find the index with the minimum weighted-class variance
	return min_within_class_variance_idx

# ##########################################################################################################################

def otsu_construct(org_img, block_r, block_c, which_img):

	img = cv2.imread(org_img, cv2.CV_LOAD_IMAGE_GRAYSCALE)				# read image to 2d array
	size = img.shape[0] * img.shape[1]									# size of the image

	hist = cv2.calcHist([img],[0],None,[256],[0,256])					# histogram of the image
	
	# Global Threshold
	glb_otsu_thres = otsu_threshold(hist, size)

	print glb_otsu_thres

	blocksize = block_r * block_c

	# break the image into list of blocks
	x = img.reshape(img.shape[0] // block_r, block_r, -1, block_c).swapaxes(1,2).reshape(-1, block_r, block_c)

	#############################################################

	# the local matrix otsu-threshold computation
	count = 0
	for i, j in enumerate(x):
		hist_j = cv2.calcHist([j],[0],None,[256],[0,256])
		# otsu_thres = threshold_otsu(j)						# for testing purpose used built-in method
		otsu_thres = otsu_threshold(hist_j, blocksize)
		
		count += 1
		print count

		for u, o in enumerate(j):
			for l, g in enumerate(o):
				if (g < otsu_thres):
					x[i][u][l] = 0
				else:
					x[i][u][l] = 1

	n, nrows, ncols = x.shape
	img_local_thres = x.reshape(img.shape[0] // nrows, -1, nrows, ncols).swapaxes(1,2).reshape(img.shape[0], img.shape[1])

	#############################################################

	#############################################################

	if (which_img == 0):	
		A1_block_r = 10
		A1_block_c = 10
	else:
		A1_block_r = 16
		A1_block_c = 16

	blocksize1 = A1_block_r * A1_block_c

	# break the image into list of blocks
	A1_x = img.reshape(img.shape[0] // A1_block_r, A1_block_r, -1, A1_block_c).swapaxes(1,2).reshape(-1, A1_block_r, A1_block_c)

	# the local matrix otsu-threshold computation
	count = 0
	for i, j in enumerate(A1_x):
		A1_hist_j = cv2.calcHist([j],[0],None,[256],[0,256])
		# otsu_thres = threshold_otsu(j)							# for testing purpose used built-in method
		otsu_thres = otsu_threshold(A1_hist_j, blocksize)
		
		count += 1
		print count

		for u, o in enumerate(j):
			for l, g in enumerate(o):
				if (g < otsu_thres):
					A1_x[i][u][l] = 0
				else:
					A1_x[i][u][l] = 1

	n, nrows, ncols = A1_x.shape
	A1_img_local_thres = A1_x.reshape(img.shape[0] // nrows, -1, nrows, ncols).swapaxes(1,2).reshape(img.shape[0], img.shape[1])

	#############################################################

	if (which_img == 0):	
		B1_block_r = 10
		B1_block_c = 10
	else:
		B1_block_r = 8
		B1_block_c = 8

	blocksize2 = B1_block_r * B1_block_c

	# break the image into list of blocks
	B1_x = img.reshape(img.shape[0] // B1_block_r, B1_block_r, -1, B1_block_c).swapaxes(1,2).reshape(-1, B1_block_r, B1_block_c)

	# the local matrix otsu-threshold computation
	count = 0
	for i, j in enumerate(B1_x):
		B1_hist_j = cv2.calcHist([j],[0],None,[256],[0,256])
		# otsu_thres = threshold_otsu(j)							# for testing purpose used built-in method
		otsu_thres = otsu_threshold(B1_hist_j, blocksize)	
		
		count += 1
		print count

		for u, o in enumerate(j):
			for l, g in enumerate(o):
				if (g < otsu_thres):
					B1_x[i][u][l] = 0
				else:
					B1_x[i][u][l] = 1

	n, nrows, ncols = B1_x.shape
	B1_img_local_thres = B1_x.reshape(img.shape[0] // nrows, -1, nrows, ncols).swapaxes(1,2).reshape(img.shape[0], img.shape[1])

	#############################################################

	if (which_img == 0):
		# break the image into list of blocks
		A1 = A1_img_local_thres.reshape(A1_img_local_thres.shape[0] // 5, 5, -1, 5).swapaxes(1,2).reshape(-1, 5, 5)
		B1 = B1_img_local_thres.reshape(B1_img_local_thres.shape[0] // 5, 5, -1, 5).swapaxes(1,2).reshape(-1, 5, 5)
	else:
		A1 = A1_img_local_thres.reshape(A1_img_local_thres.shape[0] // 1, 1, -1, 1).swapaxes(1,2).reshape(-1, 1, 1)
		B1 = B1_img_local_thres.reshape(B1_img_local_thres.shape[0] // 1, 1, -1, 1).swapaxes(1,2).reshape(-1, 1, 1)

	for i in xrange(0, len(A1)):
		if (i % 2 == 0):
			continue
		else:
			A1[i] = B1[i]

	n, nrows, ncols = A1.shape
	overlapped = A1.reshape(img.shape[0] // nrows, -1, nrows, ncols).swapaxes(1,2).reshape(img.shape[0], img.shape[1])

	#############################################################

	# print otsu_thres
	plt.figure(figsize=(16,10), facecolor='w')

	gs = gridspec.GridSpec(2, 2)

	plt.subplot(gs[0])
	plt.imshow(img, 'gray')
	plt.axis('off')
	plt.title('Original Image')

	plt.subplot(gs[1])
	plt.imshow(img >= glb_otsu_thres, 'gray')
	plt.axis('off')
	plt.title('Global Otsu Thres Applied')

	plt.subplot(gs[2])
	plt.imshow(img_local_thres, 'gray')
	plt.axis('off')
	plt.title('Otsu Threshold on local matrices without overlapping')

	plt.subplot(gs[3])
	plt.imshow(overlapped, 'gray')
	plt.axis('off')
	plt.title('Otsu Threshold on local matrices with overlapping')

	plt.show()

# #########################################################################################################################

def main():	

	# only working for these images currently because I did define
	# a general case for spliting images into blocks.

	org_img = 'images/otsu/Sudoku.png'									# img 0 to test
	otsu_construct(org_img, 7, 7, 0)

	org_img = 'images/otsu/bw.png'										# img 1 to test
	otsu_construct(org_img, 4, 4, 1)


if __name__ == '__main__':
	main()


