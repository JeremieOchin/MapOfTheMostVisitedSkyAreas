import numpy as np
import cv2 as cv


# READ BACKGROUND IMAGE
bckGrndImg = np.float32(cv.imread('X:/ASTRO/astrobinSkyMap/mixteSkyChart.png', cv.IMREAD_COLOR))

# Create image template
stackImg = np.zeros((2550, 4200, 1), np.float32)
colorStack = np.zeros((2550, 4200, 3), np.float32)
tempImg = np.zeros((2550, 4200, 1), np.float32)


with open('X:/ASTRO/astrobinSkyMap/astrobin_testfile.csv', 'r') as file:
	lines = file.read().splitlines()
	for line in lines[1:]:
		coordinates = line.split(";")
		centerX = int(3986 - 3682 * float(coordinates[0]) / 360.0)
		centerY = int(1328 - 1251 * float(coordinates[1]) / 90.0)
		radiusPic = int(float(coordinates[2]))*20
		tempImg = np.zeros((2550, 4200, 1), np.float32)
		cv.circle(tempImg, (centerX, centerY), 100, 4096, -1, cv.LINE_AA)
		stackImg += tempImg

# pxMax = np.amax(stackImg)
# stackImg /= pxMax

# ADD THE CIRCLES OVER THE BACKGROUND IMAGE IN RED CHANNEL
cv.cvtColor(stackImg, cv.COLOR_GRAY2RGB, colorStack)
colorStack[:, :, 0] = 0
colorStack[:, :, 1] = 0
bckGrndImg += colorStack

# OUTPUT THE MAP
cv.imwrite('X:/ASTRO/astrobinSkyMap/testImg.png', bckGrndImg)

