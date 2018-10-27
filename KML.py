# Write KML Header
# fp is a file pointer
def writeKMLPathHeader(fp):
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
def writeKMLPathTrailer(fp):
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


def writeKMLTurnPairHeader(fp):
	fp.write("""
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>locations.kml</name>
	<open>1</open>
	<Style id="sh_ylw-pushpin">
		<IconStyle>
			<color>ff00aa00</color>
			<scale>1.3</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<BalloonStyle>
		</BalloonStyle>
	</Style>
	<Style id="sn_ylw-pushpin">
		<IconStyle>
			<color>ff00aa00</color>
			<scale>1.1</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<BalloonStyle>
		</BalloonStyle>
	</Style>
	""")

def writeKMLPlaceMark(locationDataObj, fp):
	fp.write("""
		<Placemark>
			<name>Start Left Turn</name>
			<LookAt>
		""")
	fp.write(f"\t\t\t\t<longitude>{locationDataObj.lon}</longitude>\n")
	fp.write(f"\t\t\t\t<latitude>{locationDataObj.lat}</latitude>\n")
	fp.write(
	"""
			<altitude>0</altitude>
			<heading>0.5193636279686823</heading>
			<tilt>0</tilt>
			<range>245269.2210882676</range>
			<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
		</LookAt>
		<styleUrl>#msn_ylw-pushpin</styleUrl>
		<Point>
			<gx:drawOrder>1</gx:drawOrder>
	""")
	fp.write(f"\t\t<coordinates>{locationDataObj.outputKMLCoordinates()}</coordinates>\n")
	fp.write("""
		</Point>
	</Placemark>
	""")

def writeKMLTurnPairCoords(turnPairs, fp):
	fp.write(
		"""
		<StyleMap id="msn_ylw-pushpin">
			<Pair>
				<key>normal</key>
				<styleUrl>#sn_ylw-pushpin</styleUrl>
			</Pair>
			<Pair>
				<key>highlight</key>
				<styleUrl>#sh_ylw-pushpin</styleUrl>
			</Pair>
		</StyleMap>
		""")
	for turnPair in turnPairs:
		writeKMLPlaceMark(turnPair[0], fp)
		writeKMLPlaceMark(turnPair[1], fp)

def writeKMLTurnPairTrailer(fp):
	fp.write("""
</Document>
</kml>

	""")

# Write out entire KML file using coords fouand and a file name
# Locations is a list of LocationUpdate objects
# kmlFile is the string name of the desired output file
def writeKMLPathFile(locations, kmlFile):
	with open(kmlFile, "w+") as fp:
		writeKMLPathHeader(fp)
		writeKMLCoords(locations, fp)
		writeKMLPathTrailer(fp)

def writeKMLTurnPointsFile(turnPairs, kmlFilename):
	with open(kmlFilename, "w+") as fp:
		writeKMLTurnPairHeader(fp)
		writeKMLTurnPairCoords(turnPairs, fp)
		writeKMLTurnPairTrailer(fp)