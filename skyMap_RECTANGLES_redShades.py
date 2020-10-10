import numpy as np
import cv2 as cv
import math

# IMAGE SIZE
heightImg = 4160
widthImg = 8000

# READ BACKGROUND IMAGE
bckGrndImg = np.float32(cv.imread('X:/ASTRO/astrobinSkyMap/darkEquSkyChart.jpg', cv.IMREAD_COLOR))

# Create image template
stackImg = np.zeros((heightImg, widthImg, 1), np.float32)
mask = np.zeros((heightImg, widthImg, 1), np.float32)
heatMapBase = np.zeros((heightImg, widthImg, 1), np.uint8)
mask3 = np.zeros((heightImg, widthImg, 3), np.float32)
invMask = np.zeros((heightImg, widthImg, 1), np.float32)
invMask3 = np.zeros((heightImg, widthImg, 3), np.float32)
colorStack = np.zeros((heightImg, widthImg, 3), np.float32)
tempImg = np.zeros((heightImg, widthImg, 1), np.float32)

with open('X:/ASTRO/astrobinSkyMap/2-solutions-with-orientation-and-size_v2.csv', 'r') as file:
	lines = file.read().splitlines()
	for line in lines[1:]:
		coordinates = line.split(";")
		centerX = float(coordinates[0])
		centerY = float(coordinates[1])
		radiusPic = int(float(coordinates[2]))*1
		thetaOrient = math.radians(float(coordinates[3]))
		widthPic = float(coordinates[4])
		heightPic = float(coordinates[5])
		alphaPic = math.atan(heightPic/widthPic)
		tempImg = np.zeros((heightImg, widthImg, 1), np.float32)


		Ax = int(7781 - 7759 * (radiusPic * math.cos(alphaPic - thetaOrient) + centerX) / 360.0)
		Ay = int(1978 - 1889 * (radiusPic * math.sin(alphaPic - thetaOrient) + centerY) / 90.0)

		Bx = int(7781 - 7759 * (radiusPic * math.cos(math.pi - alphaPic - thetaOrient) + centerX) / 360.0)
		By = int(1978 - 1889 * (radiusPic * math.sin(math.pi - alphaPic - thetaOrient) + centerY) / 90.0)

		Cx = int(7781 - 7759 * (radiusPic * math.cos(math.pi + alphaPic - thetaOrient) + centerX) / 360.0)
		Cy = int(1978 - 1889 * (radiusPic * math.sin(math.pi + alphaPic - thetaOrient) + centerY) / 90.0)

		Dx = int(7781 - 7759 * (radiusPic * math.cos(-alphaPic - thetaOrient) + centerX) / 360.0)
		Dy = int(1978 - 1889 * (radiusPic * math.sin(-alphaPic - thetaOrient) + centerY) / 90.0)

		rectPts = np.array([[Dx, Dy], [Cx, Cy], [Bx, By], [Ax, Ay]], dtype=np.int32)

		cv.fillPoly(tempImg, [rectPts], 126, cv.LINE_AA)

		stackImg += tempImg

print('Stacking done')

pxMax = np.amax(stackImg)

cv.multiply(stackImg, 1 / pxMax, mask)
cv.multiply(stackImg, 255 / pxMax, stackImg)


# ADD THE CIRCLES OVER THE BACKGROUND IMAGE IN RED CHANNEL
cv.merge((stackImg, stackImg, stackImg), colorStack)
colorStack[:, :, 0] = 0
colorStack[:, :, 1] = 0

bckGrndImg += colorStack

#cv.add(bckGrndImg, colorStack, bckGrndImg)

# OUTPUT THE MAP
cv.imwrite('X:/ASTRO/astrobinSkyMap/testImg.jpg', bckGrndImg)

