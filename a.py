#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from com.dtmilano.android.adb.adbclient import AdbClient
import time
import cv2
import numpy as np


if len(sys.argv) >= 2:
    serialno = sys.argv[1]
else:
    serialno = '.*'

def touch(t):
	x = 100
	y = 100
	shell = 'input touchscreen swipe %d %d %d %d %d' % (x, y, x, y, t)
	# shell = 'input touchscreen tap %d %d %d' % (x, y, t)
	AdbClient(serialno=serialno).shell(shell)

def showImg(cimg):
	cv2.imshow('detected circles',cimg)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def drawMiddle(img, j):
	for i in xrange(len(img)):
		img[i][j] = 255

def getHighest(gray, jst, jed):
	for i in xrange(500, len(gray)):
		for j in xrange(jst, jed):
			if gray[i][j] > 100:
				return [i, j]
	print("st , ed : %d %d" % (jst, jed))

def isBetwwen(c, r, g, b):
	delta = 5
	return c[0] >= r - 5 and c[0] <= r + 5 and \
		c[1] >= g - 5 and c[1] <= g + 5 and \
		c[2] >= b - 5 and c[2] <= b + 5


def findMe(img):
	for i in xrange(600, len(img)):
		for j in xrange(len(img[0])):
			c = img[i][j]
			if isBetwwen(c, 55, 55, 55) and isBetwwen(img[i + 20][j], 112, 68, 73):
			 	return [i, j]
			# if isBetwwen(c, 55, 55, 55):
			# 	print(img[i + 20][j])
			#  	return [i, j]



imagePath = './image.png'

gray = None

imageId = 0
isTest = imageId != 0

while True:
	imagePath = "./image-%d.png" % (imageId)
	print('takeSnapshot : ' + imagePath)

	if not isTest:
		imageId += 1
		AdbClient(serialno=serialno).takeSnapshot().save(imagePath)

	img = cv2.imread(imagePath)
	if gray is None:
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	for i in xrange(len(img)):
		for j in xrange(len(img[0])):
			gray[i][j] = img[i][j][0]

	edges = cv2.Canny(gray, 20, 40)

	# circles = cv2.HoughCircles(edges[400:, :], cv2.HOUGH_GRADIENT,1,20,
 #                            param1=50,param2=30,minRadius=1,maxRadius=100)[0]
	# print(circles)
	myP = []
	myP = findMe(img)

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

	mid = len(edges[0]) / 2

	if myP[1] > mid:
		nextP = getHighest(edges, 0, mid)
	else:
		nextP = getHighest(edges, mid, len(edges[0]))

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

	dis = abs(nextP[1] - myP[1])
	print('myP : ' + str(myP))
	print("delta : %d" % (dis,))
	# showImg(img[600:1000, :])
	if isTest:
		showImg(gray[700:1300, :])
		showImg(edges[500:, :])
	if not isTest:
		touch(dis * 700 / 455)
	time.sleep(1.2)



