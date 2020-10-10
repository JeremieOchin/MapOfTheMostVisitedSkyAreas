import numpy as np
import cv2 as cv
import math


# DEFINE HEATMAP FUNCTION
def redChannelFunc(alpha):
	if alpha < 0.5:
		return 0.0
	elif alpha > 0.75:
		return 255.0
	else:
		lintVal = 255.0 * (alpha - 0.5) / 0.25
		return lintVal


def greenChannelFunc(alpha):
	if alpha < 0.25:
		lintVal = 255 * alpha / 0.25
		return lintVal
	elif alpha >= 0.25 and alpha < 0.75:
		return 255.0
	else:
		lintVal = 255.0 * (1 - alpha) / 0.25
		return lintVal


def blueChannelFunc(alpha):
	if alpha < 0.25:
		return 255.0
	elif alpha >= 0.25 and alpha < 0.5:
		lintVal = 255.0 * (0.5 - alpha) / 0.25
		return lintVal
	else:
		return 0.0


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

with open('X:/ASTRO/astrobinSkyMap/1000-solutions-with-orientation-and-size_v2.csv', 'r') as file:
	lines = file.read().splitlines()
	for line in lines[1:]:
		coordinates = line.split(";")
		centerX = float(coordinates[0])
		centerY = float(coordinates[1])
		radiusPic = float(coordinates[2])
		thetaOrient = math.radians(float(coordinates[3]))
		widthPic = float(coordinates[4])
		heightPic = float(coordinates[5])
		alphaPic = math.atan(heightPic / widthPic)
		tempImg = np.zeros((heightImg, widthImg, 1), np.float32)

		Ay = radiusPic * math.sin(alphaPic - thetaOrient) + centerY
		Ax = radiusPic * math.cos(alphaPic - thetaOrient) + centerX

		By = radiusPic * math.sin(math.pi - alphaPic - thetaOrient) + centerY
		Bx = radiusPic * math.cos(math.pi - alphaPic - thetaOrient) + centerX

		Cy = radiusPic * math.sin(math.pi + alphaPic - thetaOrient) + centerY
		Cx = radiusPic * math.cos(math.pi + alphaPic - thetaOrient) + centerX

		Dy = radiusPic * math.sin(-alphaPic - thetaOrient) + centerY
		Dx = radiusPic * math.cos(-alphaPic - thetaOrient) + centerX

		plotAx = int(7781 - 7759 * Ax / 360.0)
		plotAy = int(1978 - 1889 * Ay / 90.0)

		plotBx = int(7781 - 7759 * Bx / 360.0)
		plotBy = int(1978 - 1889 * By / 90.0)

		plotCx = int(7781 - 7759 * Cx / 360.0)
		plotCy = int(1978 - 1889 * Cy / 90.0)

		plotDx = int(7781 - 7759 * Dx / 360.0)
		plotDy = int(1978 - 1889 * Dy / 90.0)

		rectPts = np.array([[plotAx, plotAy], [plotBx, plotBy], [plotCx, plotCy], [plotDx, plotDy]], dtype=np.int32)

		cv.fillPoly(tempImg, [rectPts], 1, cv.LINE_AA)

		stackImg += tempImg

print('Stacking done')

pxMax = np.amax(stackImg)

cv.multiply(stackImg, 1 / pxMax, mask)
cv.multiply(stackImg, 255 / pxMax, stackImg)

# # GENERATE HEATMAP
print('Generating HeatMap')

vRedChannel = np.vectorize(redChannelFunc)
vGreenChannel = np.vectorize(greenChannelFunc)
vBlueChannel = np.vectorize(blueChannelFunc)

redChannelHeatMap = vRedChannel(mask)
greenChannelHeatMap = vGreenChannel(mask)
blueChannelHeatMap = vRedChannel(mask)

colorStack = cv.merge((blueChannelHeatMap, greenChannelHeatMap, redChannelHeatMap))

# ADD THE CIRCLES OVER THE BACKGROUND IMAGE IN RED CHANNEL
cv.merge((mask, mask, mask), mask3)

# invMask = 1 - mask
# cv.merge((invMask, invMask, invMask), invMask3)
# cv.multiply(bckGrndImg, invMask3, bckGrndImg)

bckGrndImg += colorStack

# OUTPUT THE MAP
cv.imwrite('X:/ASTRO/astrobinSkyMap/testImg.jpg', bckGrndImg)

