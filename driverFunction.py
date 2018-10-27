from LocationData import LocationData
import DetectLeftTurns
import KML

inputFile = "testData.txt"
outputPathFile = "locations.kml"
outputPointsFile = "turnPoints.kml"

def processFile(gpsFilename):
	locationUpdates = []
	with open(gpsFilename) as fp:
		lines = fp.readlines()
		for line in lines:
			# Translate the GPRMC lines. GPRMC function checks for the right line,
			# so i pass it every line
			locationUpdate = LocationData.translateGPRMC(line)
			if locationUpdate:
				if len(locationUpdates) > 0:
					lastLocation = locationUpdates[len(locationUpdates)-1]
					if lastLocation.lon == locationUpdate.lon and lastLocation.lat == locationUpdate.lat:
						continue
					else:
						locationUpdates.append(locationUpdate)
				else:
					locationUpdates.append(locationUpdate)
			else:
				continue
				
	return locationUpdates


locationUpdates = processFile(inputFile)
turnPairs = DetectLeftTurns.findLeftTurns(locationUpdates)
print("LEFT TURNS:")
for turnPair in turnPairs:
	print(f"-----\n{turnPair[0].lat}, {turnPair[0].lon}\n{turnPair[1].lat}, {turnPair[1].lon}\n)")

# Write out path of car
KML.writeKMLPathFile(locationUpdates, outputPathFile)
# write out points for left turns
KML.writeKMLTurnPointsFile(turnPairs, outputPointsFile	)
