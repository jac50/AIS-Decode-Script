#	python decode.py
#	usage: decode.py [-h] [-AIS | -cat10] [AISFilePath] [Cat10FilePath]

#	AIS and Cat 10 Message Decoder

#	positional arguments:
# 	 AISFilePath          Path to the AIS Data File
# 	 Cat10FilePath        Path to the Cat 10 Wireshark Capture File (PCAP)

#	optional arguments:
# 	 -h, --help           show this help message and exit
# 	 -AIS, --AISonly      Optional Flag if only Cat 10 decoded is required
# 	 -cat10, --CAT10only  Optional Flag if only Cat 10 decoded is required

#	Note: If only AIS or Cat10 decoding is required, just add the one filepath.


import argparse
import csv
import simpleais
import subprocess
import math
import os
from datetime import datetime

def main():	
	startTime = datetime.now() #Start Timer to see how long script takes to run

	#Sets up the argument parser
	parser = argparse.ArgumentParser(description='AIS and Cat 10 Message Decoder', epilog="Note: If only AIS or Cat10 decoding is required, just add the one filepath.")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-AIS", "--AISonly", action="store_true", help="Optional Flag if only Cat 10 decoded is required")
	group.add_argument("-CAT10", "--CAT10only", action="store_true",help="Optional Flag if only Cat 10 decoded is required")
	parser.add_argument('AISFilePath', nargs='?',default='AIS.csv', help='Path to the AIS Data File')
	parser.add_argument('Cat10FilePath', nargs='?',default='Cat10TrackData.pcap',help='Path to the Cat 10 Wireshark Capture File (PCAP)')
	
	#Parse arguments using ArgParse and check if paths are valid
	args = parser.parse_args()
	paths=[]
	paths = parseArguments(args)

	
	if args.CAT10only == True:
		Cat10Decode(paths[1])
	elif args.AISonly == True:
		AISDecode(paths[0])
	else:
		AISDecode(paths[0])
		Cat10Decode(paths[1])
	
	endTime = datetime.now()
	print("Script took %.4f seconds to complete" % ((endTime - startTime).total_seconds()))
	
def parseArguments(args):

	if args.AISonly == True:
		if os.path.isfile(args.AISFilePath) == False:
			return False
	elif args.CAT10only == True:
		if os.path.isfile(args.Cat10FilePath) == False:
			return False
	else:
		if os.path.isfile(args.AISFilePath) == False or (os.path.isfile(args.Cat10FilePath) == False):
			return False
		
	return [args.AISFilePath, args.Cat10FilePath]

def cleanFiles():
	print("Clean up directory..")
	os.remove("Cat10Decoded.txt")	

def AISDecode(path):
	print("AIS Decoding Started..")
	fInput = open(path, "r", newline='')
	fOutput = open('AISDecoded.csv',"w", newline='')
	AISReader = csv.reader(fInput,delimiter=',')
	AISWriter = csv.writer(fOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	AISWriter.writerow(["MMSI","Latitude","Longitude","COG","SOG", "Time"])
	for row in AISReader:
		message = row[0]		
		decodedMsg = simpleais.parse(message)
		if decodedMsg is None:
			continue
		AISWriter.writerow([decodedMsg['mmsi'],decodedMsg['lat'], decodedMsg['lon'], decodedMsg['course'], decodedMsg['speed'], row[1]])
	
	print("AIS Decoded")
	
def Cat10Decode(path):
	print("Cat10 Decoding started...")
	fCat10Decoded = open('Cat10Decoded.txt',"w", newline='')
	
	error = subprocess.call(['asterix.exe','-P','-l' '-v','-f',path],stdout = fCat10Decoded)
	print("Asterix program loaded")
	if error != 0:
		print("Error detected when loading asterix.exe. Program halted.")
		return 1
	fCat10Decoded.close()
	print("Asterix decoded. File being converted to CSV")
	
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
	fCat10Decoded.close()
	fCat10CSV.close()
	print("Cat10 decoding finished!")
	cleanFiles()
		
def formatTime(time):
	#Time is in 1/128 of a second
	
	seconds = int(time) / 128 #seconds
	minutes = seconds / 60
	hours = minutes / 60
	timeList = [math.floor(hours), math.floor(minutes%60),seconds % 60] #Floor not required for seconds,as milliseconds are also required.
	timeStr = ':'.join(str(x) for x in timeList)
	return(timeStr)

if __name__ == "__main__":
	main()
	