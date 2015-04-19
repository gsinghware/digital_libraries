# Gurpreet Singh
# Digital Libraries
# Assignment 1, problem 3

import cv2
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from skimage.filters import threshold_adaptive
from skimage import data

def coin_recognize(image, itera, coin_area, gs, where):
	coin = cv2.imread(image, 0)
	
	# apply blur to remove any noise
	coin_without_noise = cv2.blur(coin,(10, 10))

	# apply threshold to seperate the background and the foreground
	coin_thresh_without_noise = cv2.adaptiveThreshold(coin_without_noise, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 1)

	# apply closing of image dilation and then erosion
	# this makes the area around the coins to become filled. 
	block_of_1s = np.ones((2, 2), np.uint8)
	closing = cv2.morphologyEx(coin_thresh_without_noise, cv2.MORPH_CLOSE, block_of_1s, iterations=itera)

	# make a copy of the image after closing
	closing_cpy = closing.copy()

	# find all the contours in the closing image
	contours, hierarchy = cv2.findContours(closing_cpy,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	font = cv2.FONT_HERSHEY_SIMPLEX

	# for every contours, if the area of the matches the area of coin
	# then draw an ellipse around the area.
	for cont in contours:
		area = cv2.contourArea(cont)
		if ((area > coin_area[0][0] and area < coin_area[0][1]) and (len(cont) > 3)):
			ellipse = cv2.fitEllipse(cont)
			cv2.ellipse(coin, ellipse, (1,0,0), 2)
			cv2.putText(coin, coin_area[0][2], (int(ellipse[0][0]), int(ellipse[0][1])), font, 1, (255,255,255), 2)

		elif ((area > coin_area[1][0] and area < coin_area[1][1]) and (len(cont) > 3)):
			ellipse = cv2.fitEllipse(cont)
			cv2.ellipse(coin, ellipse, (1,0,0), 2)
			cv2.putText(coin, coin_area[1][2], (int(ellipse[0][0]), int(ellipse[0][1])), font, 1,(255,255,255), 2)

	plt.subplot(where[0])
	plt.imshow(coin, 'gray')
	plt.axis('off')
	plt.title('Coin')

	plt.subplot(where[1])
	plt.imshow(coin_without_noise, 'gray')
	plt.axis('off')
	plt.title('Coin without noise (blur, averaging)')

	plt.subplot(where[2])
	plt.imshow(coin_without_noise >= coin_thresh_without_noise, 'gray')
	plt.axis('off')
	plt.title('Coin adaptive threshold applied')

	plt.subplot(where[3])
	plt.imshow(closing, 'gray')
	plt.axis('off')
	plt.title('Coin after closing (9 iterations)')

def main():
	plt.figure(figsize=(16, 10), facecolor='w')
	gs = gridspec.GridSpec(3, 4)

	# coin_recognize(img, closing_iteration, list with area of each coin in image, gs, list with placement in the figure)
	coin_recognize('images/coins/nickel_dime.jpg', 9, [(5000, 9000, 'Dime'), 
					(9000, 13000, 'Nickel')], gs, [gs[0, 0], gs[0, 1], gs[0, 2], gs[0, 3]])

	coin_recognize('images/coins/nickel_quarter.jpg', 9, [(5000, 10000, 'Nickel'), 
					(9000, 13000, 'Quarter')], gs, [gs[1, 0], gs[1, 1], gs[1, 2], gs[1, 3]])

	coin_recognize('images/coins/quarter_dime.jpg', 9, [(7000, 8000, 'dime'), 
					(9000, 13000, 'Quarter')], gs, [gs[2, 0], gs[2, 1], gs[2, 2], gs[2, 3]])
	
	plt.show()



if __name__ == '__main__':
	main()