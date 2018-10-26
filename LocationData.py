import math

"""
Helper class to hold universal data
Basic constructor with all fields, but the most useful thing
  is probably constructing this class from 'translateGPRMC', which
  takes any string. If it detects that it's in the given GPRMC format
  than it will convert it to a LocationData Object and return the new
  object.
  This function can be called like so:
     locDataInstance = LocationData.translateGPRMC("exampleStr")
"""
class LocationData:
	# Basic Constructor
	def __init__(self, lon, lat, speed, angle, time):
		self.lon = lon
		self.lat = lat
		self.speed = speed
		self.angle = angle
		self.time = time

	def __str__(self):
		return (f"Longitude: {self.lon}" +
				f" Latitude: {self.lat}" + 
				f" Speed: {self.speed}" + 
				f" Angle: {self.angle}" + 
				f" Time: {self.time}" )

	def outputKMLCoordinates(self):
		return f"{self.lon},{self.lat},{self.speed}"


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
			# I will convert to KmPH, not sure what to do
			oneKnotInKPH = 1.852
			speed = float(gpsTokens[7])*oneKnotInKPH

			# Get Angle of vehicle
			angle = float(gpsTokens[8])
		
			return LocationData( longitudeDegrees, latitudeDegrees, speed, angle, time)

	# Translates a GPS string (NOT RMC OR GGA) and returns an instance of a new class
	# Kinda useless but I'll leave it in here to cause confusion
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

	# Find the euclidian distance between any two coords
	# RETURNS DISTANCE METERS!
	def distanceBetweenTwoCoords(locData1, locData2):
		# One degree of latitude is 111111 meters everywhere on the globe
		latDegreeInMeters = 111111
		latDist = (locData1.lat - locData2.lat)*latDegreeInMeters

		# One degree of longitude is dependent on your latitude
		lonDist = (locData1.lon - locData2.lon)*math.cos(math.radians(locData2.lat))*latDegreeInMeters

		# One degree of longitude is different depending on where you're on the globe		
		return math.sqrt( lonDist**2 + latDist**2 )

	# Find the euclidian distance between this point (self) and
	#   another point (otherPoint)
	# RETURNS DISTANCE METERS!
	def distanceToCoord(self, otherPoint):
		# One degree of latitude is 111111 meters everywhere on the globe
		latDegreeInMeters = 111111
		latDist = (self.lat - otherPoint.lat)*latDegreeInMeters

		# One degree of longitude is dependent on your latitude
		lonDist = (self.lon - otherPoint.lon)*math.cos(math.radians(otherPoint.lat))*latDegreeInMeters

		# One degree of longitude is different depending on where you're on the globe		
		return math.sqrt( lonDist**2 + latDist**2 )