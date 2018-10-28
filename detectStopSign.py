from LocationData import LocationData
import KML
import pandas as pd
import matplotlib.pyplot as plt
dataOutputFile = "dataframe.csv"
outputStopsFile = "stopPoints.kml"

def writeKMLPlaceStop(locationDataObj, fp):
    fp.write(f"""
        <Placemark>
            <name>Stop</name>
            <description>{locationDataObj.speed}</description>
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

def objectify(dfRow):
    locationObj = LocationData(dfRow['lon'], dfRow['lat'], dfRow['speed'], dfRow['angle'], dfRow['time'])
    return locationObj

def outputStops(stopDF, fp):
    KML.writeKMLTurnPairHeader(fp)
    for index, row in stopDF.iterrows():
        writeKMLPlaceStop(objectify(row), fp)
    KML.writeKMLTurnPairTrailer(fp)

def detectStops(data):
    allStops = data[data['speed'] < 1]
    allStops = allStops.assign(distanceToLast=0)
    lastLoc = None
    for index, row in allStops.iterrows():
        if lastLoc is not None:
            currLoc = objectify(row)
            stopDistance = currLoc.distanceToCoord(lastLoc)
            lastLoc = currLoc
            allStops.loc[index, 'distanceToLast'] = stopDistance
        else:
            lastLoc = objectify(row)
    distanceThreshold = 10
    stopSigns = allStops[allStops['distanceToLast'] > distanceThreshold]

    plot = allStops.plot(x='Unnamed: 0', y='distanceToLast', title='Distance Between Stops')
    plot.set_ylabel('Distance (m) since last stop in data')
    plt.show()

    return stopSigns

def main():
    data = pd.read_csv(dataOutputFile)
    stopSigns = detectStops(data)
    fp = open(outputStopsFile, 'w')
    outputStops(stopSigns, fp)
    stopSigns.to_csv('stopDistance.csv')

    plot = data.plot(x='Unnamed: 0', y='speed', title='Speed during trip')
    plot.set_ylabel('Speed in KPH')
    plt.show()


if __name__ == "__main__":
    main()