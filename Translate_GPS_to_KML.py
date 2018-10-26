
inputFile = "testData.txt"
outputFile = "locations.kml"

latitudeInMeters = 111000

# Helper class to hold universal data
# May turn out useful for storing data between GPS and KML state
# May turn out redundant, I dunno
class LocationData:
	# Basic Constructor
	def __init__(self, lng, lat, speed, angle, time):
		self.lng = lng
		self.lat = lat
		self.speed = speed
		self.angle = angle
		self.time = time

	def __str__(self):
		return (f"Longitude: {self.lng}" +
				f" Latitude: {self.lat}" + 
				f" Speed: {self.speed}" + 
				f" Angle: {self.angle}" + 
				f" Time: {self.time}" )

	def outputKMLCoordinates(self):
		return f"{self.lng},{self.lat},{self.speed}"

#$GPRMC,193049.800,A,4305.1558,N,07740.7774,W,0.16,200.90,130818,,,A*71 
#lng=-77.679618, lat=43.085929, altitude=199.20, speed=0.22, satellites=5, angle=179.4800, fixquality=1
def translateGPRMC(gpsString):
	gpsTokens = gpsString.split(',')
	if gpsTokens[0] == "$GPRMC":
		# Get the time
		time = float(gpsTokens[1])

		# Get Latitude
		latitudeString = gpsTokens[3]
		latitudeDegrees = int(latitudeString[0:2])
		latitudeMinutes = float(latitudeString[2:9])
		# Must convert minutes to degrees then add
		latitudeDegrees += (1/60)*latitudeMinutes
		# Get latitude North or South
		latitudeDegrees *= -1 if gpsTokens[4] == "S" else 1

		# Get Longitude
		longitudeString = gpsTokens[5]
		longitudeDegrees = int(longitudeString[0:3])
		longitudeMinutes = float(longitudeString[3:10])
		# Must convert minutes degress then add
		longitudeDegrees += (1/60)*longitudeMinutes
		# Get longitude East or West
		longitudeDegrees *= -1 if gpsTokens[6] == "W" else 1

		# Get speed, which is initially in Knots
		# I will convert to MPH, not sure what to do
		oneKnotInMPH = 1.15078
		speed = float(gpsTokens[7])*oneKnotInMPH

		# Get Angle of vehicle
		angle = float(gpsTokens[8])
	
		return LocationData(latitudeDegrees, longitudeDegrees, speed, angle, time)

# Translates a GPS string (NOT RMC OR GGA) and returns an instance of a new class
def translateGPSString(gpsString):
	gpsTokens = gpsString.split(',')
	# Looking only at the lng=-77.67 type format
	if len(gpsTokens) == 7:
		locationDataList = []
		for token in gpsTokens:
			strTokens = token.split('=')
			if "." in strTokens[1]:
				locationDataList.append(float(strTokens[1]))
			else:
				locationDataList.append(int(strTokens[1]))

		return LocationData(locationDataList[0], locationDataList[1], 
						locationDataList[2], locationDataList[3], 
						locationDataList[4], locationDataList[5], 
						locationDataList[6] )
	else:
		return None

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
			locationUpdate = translateGPRMC(line)
			if locationUpdate:
				if len(locationUpdates) > 0:
					lastLocation = locationUpdates[len(locationUpdates)-1]
					if lastLocation.lng == locationUpdate.lng and lastLocation.lat == locationUpdate.lat:
						print("---------------------")
						print(locationUpdate)
						print(lastLocation)
						print(locationUpdate.speed)
						print("---------------------")
						continue
					else:
						locationUpdates.append(locationUpdate)
				else:
					locationUpdates.append(locationUpdate)
			else:
				continue
				
	return locationUpdates



locationUpdates = processFile(inputFile)
writeKMLFile(locationUpdates, outputFile)
