from LocationData import LocationData

inputFile = "testData.txt"
outputFile = "locations.kml"

# Write KML Header
# fp is a file pointer
def writeKMLHeader(fp):
	kmlHeader = '<?xml version="1.0" encoding="UTF-8"?>\n'
	kmlHeader += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
	kmlHeader += '<Document>\n'
	kmlHeader += '\t<Style id="yellowPoly">\n'
	kmlHeader += '\t\t<LineStyle>\n'
	kmlHeader += '\t\t\t<color>Af00ffff</color>\n'
	kmlHeader += '\t\t\t<width>6</width>\n'
	kmlHeader += '\t\t</LineStyle>\n'
	kmlHeader += '\t\t<PolyStyle>\n'
	kmlHeader += '\t\t\t<color>7f00ff00</color>\n'
	kmlHeader += '\t\t</PolyStyle>\n'
	kmlHeader += '\t</Style>\n'
	kmlHeader += '\t<Placemark><styleUrl>#yellowPoly</styleUrl>\n'
	kmlHeader += '\t\t<LineString>\n'
	kmlHeader += '\t\t<Description>Speed in MPH, not altitude.</Description>\n'
	kmlHeader += '\t\t<extrude>1</extrude>\n'
	kmlHeader += '\t\t<tessellate>1</tessellate>\n'
	kmlHeader += '\t\t<altitudeMode>relative</altitudeMode>\n'
	kmlHeader += '\t\t\t<coordinates>\n'
	fp.write(kmlHeader)

# Write KML Trailer
# fp is a file pointer
def writeKMLTrailer(fp):
	kmlTrailer = '\t\t\t</coordinates>\n'
	kmlTrailer += '\t\t</LineString>\n'
	kmlTrailer += '\t</Placemark>\n'
	kmlTrailer += '</Document>\n'
	kmlTrailer += '</kml>\n'
	fp.write(kmlTrailer)


# Write out all the coordinates for the KML file
# Locations is a list of LocationUpdate objects
# FP is a file pointer
def writeKMLCoords(locations, fp):
	for location in locations:
		fp.write(f"\t\t{location.outputKMLCoordinates()}\n")

# Write out entire KML file using coords fouand and a file name
# Locations is a list of LocationUpdate objects
# kmlFile is the string name of the desired output file
def writeKMLFile(locations, kmlFile):
	with open(kmlFile, "w+") as fp:
		writeKMLHeader(fp)
		writeKMLCoords(locations, fp)
		writeKMLTrailer(fp)

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
						#print("---------------------")
						#print(locationUpdate)
						#print(lastLocation)
						#print(locationUpdate.speed)
						#print("---------------------")
						continue
					else:
						locationUpdates.append(locationUpdate)
				else:
					locationUpdates.append(locationUpdate)
			else:
				continue
				
	return locationUpdates


#def __init__(self, lon, lat, speed, angle, time)
#-77.67530935350142,43.09912741431598,161.9482426272082 -77.66910010272682,43.09402034739996,159.2874976941509 
locData1 = LocationData(-77.67530935350142, 43.09912741431598, 0, 0, 0)
locData2 = LocationData(-77.66910010272682, 43.09402034739996, 0, 0, 0)

print(locData1)
print(locData2)

print(LocationData.distanceBetweenTwoCoords(locData1, locData2))
print(locData1.distanceToCoord(locData2))

locationUpdates = processFile(inputFile)
writeKMLFile(locationUpdates, outputFile)
