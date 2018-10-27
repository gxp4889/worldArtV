"""
Filler
"""
from pprint import pprint
import math

#hhmmss
def addTime(timeStampInt, timeToAddInSeconds):
	timeStampStr = str(timeStampInt)
	hours = int(timeStampStr[0:2])
	minutes = int(timeStampStr[2:4])
	seconds = int(timeStampStr[4:6]) + timeToAddInSeconds
	# handle overflow
	if seconds > 59:
		seconds = seconds % 60
		minutes +=1
		if minutes > 59:
			minutes = minutes % 60
			hours += 1

	return int(str(hours) + str(minutes) + str(seconds))

def addDistance(locPoint1, locPoint2):
	return locPoint1.distanceToCoord(locPoint2)

def findAngleDifference(locPoint1, locPoint2):
	angleDelta = locPoint1.angle - locPoint2.angle
	if angleDelta > 180:
		return 360 - angleDelta
	elif angleDelta < -180:
		return -360 - angleDelta
	else:
		return angleDelta


def findLeftTurns(locationDataPoints):
	turnPairs = []
	i = 0
	while i < len(locationDataPoints):
		currLoc = locationDataPoints[i]
		stopTime = addTime(currLoc.time, 30)
		j=i
		while j < len(locationDataPoints):
			tempLoc = locationDataPoints[j]
			if addDistance(currLoc, tempLoc) >= 30:
				if findAngleDifference(currLoc, tempLoc) >= 75:
					turnPairs.append([currLoc, tempLoc])
				i=j
				break
			j+=1
		i+=1
	return turnPairs