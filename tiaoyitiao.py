#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from com.dtmilano.android.adb.adbclient import AdbClient
import time
import cv2
import math
import numpy as np
from multiprocessing import freeze_support

freeze_support()

if len(sys.argv) >= 2:
    serialno = sys.argv[1]
else:
    serialno = '.*'

def touch(t):
	x = 500
	y = 500
	shell = 'input touchscreen swipe %d %d %d %d %d' % (x, y, x, y, t)
	print t
	# shell = 'input touchscreen tap %d %d %d' % (x, y, t)
	AdbClient(serialno=serialno).shell(shell)

def showImg(cimg):
	cv2.imshow('detected circles',cimg)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def showImg2(cimg):
	cv2.imshow('detected circles',cimg)
	cv2.waitKey(1000)

def drawMiddle(img, j):
	for i in xrange(len(img)):
		img[i][j] = 255

def getHighest(gray, jst, jed):
	for i in xrange(500, len(gray)):
		for j in xrange(jst, jed):
			if gray[i][j] > 50:
				return [i, j]
	print("st , ed : %d %d" % (jst, jed))

def getHighest2(gray, jst, jed):
	left = getHighest(gray, jst, jed)
	right = -1
	for j in xrange(jed - 1, jst, -1):
		if gray[left[0]][j] > 50:
			right = [left[0], j]
			break
	if right == -1:
		print left
	return [left[0], (left[1] + right[1]) / 2]
	print("st , ed : %d %d" % (jst, jed))

def isBetwwen(c, r, g, b):
	delta = 5
	return c[0] >= r - 5 and c[0] <= r + 5 and \
		c[1] >= g - 5 and c[1] <= g + 5 and \
		c[2] >= b - 5 and c[2] <= b + 5

def isBetwwen(c, r, g, b, d):
	return c[0] >= r - d and c[0] <= r + d and \
		c[1] >= g - d and c[1] <= g + d and \
		c[2] >= b - d and c[2] <= b + d

def findMe(img):
	for i in xrange(600, len(img)):
		for j in xrange(len(img[0])):
			c = img[i][j]
			if isBetwwen(c, 55, 55, 55, 10) and isBetwwen(img[i + 20][j], 112, 68, 73, 10):
				img[i - 1][j] = [255, 0, 0]
			 	return [i, j]
			# if isBetwwen(c, 55, 55, 55):
			# 	print(img[i + 20][j])
			#  	return [i, j]

def findMe2(img):
	left = findMe(img)
	for j in xrange(len(img[0]) - 1, 0, -1):
		c = img[left[0]][j]
		if isBetwwen(c, 55, 55, 55, 10) and isBetwwen(img[left[0] + 20][j], 136, 88, 97, 30):
			img[left[0] - 1][j] = [255, 0, 0]
			right = [left[0], j]
			break
	return [left[0], (left[1] + right[1]) / 2]
			# if isBetwwen(c, 55, 55, 55):
			# 	print(img[i + 20][j])
			#  	return [i, j]

imagePath = './image.png'

gray = None

imageId = 0
isTest = imageId != 0

centerCols = 562

lastDir = True # true right  false left

# kernel1 = np.array([(3, 10, 3), (0, 0, 0) , (-3, -10, -3)])
# kernel2 = np.array([(-3, -10, -3), (0, 0, 0) , (3, 10, 3)])

kernel1 = np.array([(0, 10, 0), (0, 0, 0), (0, -10, 0)])
kernel2 = np.array([(0, -10, 0), (0, 0, 0), (0, 10, 0)])

while True:
	imagePath = "./image-%d.png" % (imageId)
	print('takeSnapshot : ' + imagePath)

	if not isTest:
		imageId += 1
		AdbClient(serialno=serialno).takeSnapshot().save(imagePath)

	img = cv2.imread(imagePath)

	# if gray is None:
	# 	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
	# for i in xrange(len(img)):
	# 	for j in xrange(len(img[0])):
	# 		gray[i][j] = img[i][j][0]

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# edges = gray.copy()
	# for i in xrange(len(img) - 1):
	# 	for j in xrange(len(img[0])):
	# 		edges[i][j] = 0
	# 		distB = img[i + 1][j][0] - img[i][j][0]
	# 		distG = img[i + 1][j][1] - img[i][j][1]
	# 		distR = img[i + 1][j][2] - img[i][j][2]
	# 		if distB == 255:
	# 			distB = 0
	# 		if distG == 255:
	# 			distG = 0
	# 		if distR == 255:
	# 			distR = 0
	# 		temp = distB * distB + distG * distG + distR * distR
	# 		#temp *= 20
	# 		if temp > 255:
	# 			edges[i][j] = 255
	# 		else:
	# 			edges[i][j] = temp

	#edges = cv2.Sobel(gray, cv2.CV_8U, 0, 1, 3)

	splitImg = cv2.split(img)
    #
	# imageEdgeWritePath = "./debug_image-%d-1.png" % (imageId)
	# cv2.imwrite(imageEdgeWritePath, splitImg[0])
    #
	# imageEdgeWritePath = "./debug_image-%d-2.png" % (imageId)
	# cv2.imwrite(imageEdgeWritePath, splitImg[1])
    #
	# imageEdgeWritePath = "./debug_image-%d-3.png" % (imageId)
	# cv2.imwrite(imageEdgeWritePath, splitImg[2])


	edges1_0 = cv2.filter2D(splitImg[0], -1, kernel1)
	edges2_0 = cv2.filter2D(splitImg[0], -1, kernel2)

	edges1_1 = cv2.filter2D(splitImg[1], -1, kernel1)
	edges2_1 = cv2.filter2D(splitImg[1], -1, kernel2)

	edges1_2 = cv2.filter2D(splitImg[2], -1, kernel1)
	edges2_2 = cv2.filter2D(splitImg[2], -1, kernel2)

	# imageEdgeWritePath = "./debug_image-%d--0.png" % (imageId)
	# cv2.imwrite(imageEdgeWritePath, edges1_0)
	# imageEdgeWritePath = "./debug_image-%d--1.png" % (imageId)
	# cv2.imwrite(imageEdgeWritePath, edges2_0)
	# imageEdgeWritePath = "./debug_image-%d--2.png" % (imageId)
	# cv2.imwrite(imageEdgeWritePath, edges1_1)
	# imageEdgeWritePath = "./debug_image-%d--3.png" % (imageId)
	# cv2.imwrite(imageEdgeWritePath, edges2_1)
	# imageEdgeWritePath = "./debug_image-%d--4.png" % (imageId)
	# cv2.imwrite(imageEdgeWritePath, edges1_2)
	# imageEdgeWritePath = "./debug_image-%d--5.png" % (imageId)
	# cv2.imwrite(imageEdgeWritePath, edges2_2)


	# edges = edges1_0 + edges2_0 + edges1_1 + edges2_1 + edges1_2 + edges2_2
	edges = np.maximum(edges1_0, edges2_0)
	edges = np.maximum(edges, edges1_1)
	edges = np.maximum(edges, edges2_1)
	edges = np.maximum(edges, edges1_2)
	edges = np.maximum(edges, edges2_2)


	# imageEdgeWritePath = "./debug_image-%d-9.png" % (imageId)
	# cv2.imwrite(imageEdgeWritePath, edges)
	#edges = cv2.Canny(gray, 3, 10)

	# circles = cv2.HoughCircles(edges[400:, :], cv2.HOUGH_GRADIENT,1,20,
 #                            param1=50,param2=30,minRadius=1,maxRadius=100)[0]
	# print(circles)
	myP = []
	myP = findMe2(img)

	if not isTest:
		for i in xrange(myP[0] - 2, myP[0] + 63):
			for j in xrange(myP[1] - 35, myP[1] + 35):
				edges[i][j] = 0

	# for i in xrange(len(circles)):
	# 	c = circles[i]
	# 	x = int(c[0])
	# 	y = int(c[1]) + 400
	# 	# r = int(c[2] + 20)
	# 	# if r < 47 or r > 53:
	# 	# 	continue
	# 	# print(c)
	# 	# showImg(img[y-r:y+r, x-r:x+r])

	# 	myP = [y, x]
	# 	r = int(c[2] + 3)
	# 	for i in xrange(y - r, y + r):
	# 		for j in xrange(x - r, x + r):
	# 			gray[i][j] = 0

	# 	break

	mid = len(edges[0]) / 2 #centerCols #len(edges[0]) / 2

	nowDir = True

	if myP[1] > mid:
		nextP = getHighest2(edges, 0, mid)
		nowDir = False
	else:
		nextP = getHighest2(edges, mid, len(edges[0]))
		nowDir = True;

	print('nextP : ' + str(nextP))
	# delta = 140
	# if nextP[1] < len(edges[0]) / 2:
	# 	# left
	# 	mid = len(edges[0]) / 2 + delta
	# 	myP = getHighest(edges, mid, len(edges[0]))
	# 	drawMiddle(edges, mid)
	# else:
	# 	mid = len(edges[0]) / 2 - delta
	# 	myP = getHighest(edges, 0, mid)
	# 	drawMiddle(edges, mid)
	if nowDir == lastDir:
		dis = abs(nextP[1] - myP[1])
	else:
		dis = abs(nextP[1] - centerCols) * 2



	print('myP : ' + str(myP))
	print("delta : %d" % (dis,))
	# showImg(img[600:1000, :])
	if isTest:
		showImg(gray[700:1300, :])
		showImg(edges[500:, :])
	if not isTest:
		touch(dis * 810 * 1.0 / 452)
	time.sleep(1.2)


	cv2.line(img, (myP[1], 700), ( myP[1], 1300), (0, 0, 255), 1)
	cv2.line(img, (nextP[1], 700), (nextP[1], 1300), (0, 0, 255), 1)
	if nowDir != lastDir:
		if nowDir == True:
			cv2.line(img, (centerCols - dis / 2, 700), (centerCols - dis / 2, 1300), (255, 0, 0), 1)
		else:
			cv2.line(img, (centerCols + dis / 2, 700), (centerCols + dis / 2, 1300), (255, 0, 0), 1)
	lastDir = nowDir
	imageWritePath = "./debug_image-%d-%d.png" % (imageId, dis)
	cv2.imwrite(imageWritePath, img)
	imageEdgeWritePath = "./debug_image-%d-edge.png" % (imageId)
	cv2.imwrite(imageEdgeWritePath, edges)
	imageGrayWritePath = "./debug_image-%d-gray.png" % (imageId)
	cv2.imwrite(imageGrayWritePath, gray)
	#showImg2(img[700:1300, :])
	#time.sleep(0.5)
