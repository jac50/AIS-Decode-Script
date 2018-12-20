import argparse
import csv
import simpleais
import subprocess
import math
from datetime import datetime

#import asterix_decoder

def main():	
	startTime = datetime.now()
	#Parse script arguments

	#parser = argparse.ArgumentParser(description='Decoding AIS messages')
	#parser.add_argument('filepath',
				#	   help='Test')

	
	#args = parser.parse_args()
	#AISDecode()
	Cat10Decode()
	
	endTime = datetime.now()
	print("Script took %d seconds to complete" % (endTime - startTime).total_seconds())
	

	

def AISDecode():
	print("AIS Decoded Started..")
	fInput = open("Test.csv", "r", newline='')
	fOutput = open('AISDecoded.csv',"w", newline='')
	AISReader = csv.reader(fInput,delimiter=',')
	AISWriter = csv.writer(fOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	

	for row in AISReader:
		message = row[0]		
		decodedMsg = simpleais.parse(message)
		if decodedMsg is None:
			continue
		AISWriter.writerow([decodedMsg['mmsi'],decodedMsg['lat'], decodedMsg['lon'], decodedMsg['course'], decodedMsg['speed'], row[1]])
	
	print("AIS Decoded")
	
def Cat10Decode():
	print("Cat10 Decoding started...")
	fCat10Decoded = open('Cat10Decoded.txt',"w", newline='')
	subprocess.call(['C:\\Users\\khhqjames.cox\\Documents\\Projects\\Tasks\\asterix_win64_2.2.1\\asterix.exe','-P','-l','-f','Cat10TrackData.pcap'],stdout = fCat10Decoded,stderr = None)
	fCat10Decoded.close()
	
	fCat10Decoded = open('Cat10Decoded.txt',"r", newline='')
	fCat10CSV = open('Cat10Decoded.csv',"w", newline='')
	csvWriter = csv.writer(fCat10CSV)
	flag = 0
	csvWriter.writerow(["Time","Latitude","Longitude","SOG (NM/s)", "COG", "Track Number"])
	row = []
	for line in fCat10Decoded:
	
		lineList = line.split(' ')

		if lineList[0] == "Asterix.CAT010.010.SAC":
			row = []
			continue
		if lineList[0] == "Asterix.CAT010.140.ToD":
			timeFormatted = formatTime(lineList[1])
			row.append(timeFormatted)
			continue
		elif lineList[0] == "Asterix.CAT010.041.Latitude":
			row.append(lineList[7].split('(')[1])
			continue
		elif lineList[0] == "Asterix.CAT010.041.Longitude":
			row.append(lineList[7].split('(')[1])
			continue
		elif lineList[0] == "Asterix.CAT010.200.GS":
			row.append(lineList[2].split('(')[1])
			continue
		elif lineList[0] == "Asterix.CAT010.200.TA":
			row.append(lineList[2].split('(')[1])
			continue
		elif lineList[0] == "Asterix.CAT010.161.TrkNb":
			row.append(lineList[1].rstrip())
			flag = 1
			continue
		
		if flag == 1:
			csvWriter.writerow(row)
			row = []
			flag = 0
			
	print("Cat10 decoding finished!")
		
def formatTime(time):
	#Time is in 1/128 of a second
	
	seconds = int(time) / 128 #seconds
	minutes = seconds / 60
	hours = minutes / 60
	timeList = [math.floor(hours), math.floor(minutes%60),seconds % 60]
	timeStr = ':'.join(str(x) for x in timeList)
	return(timeStr)
	
	
	
	
	
	









if __name__ == "__main__":
	main()
	