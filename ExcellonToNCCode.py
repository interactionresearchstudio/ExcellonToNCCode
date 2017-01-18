# open excellon file
# read every line
# if line contains inch, set mode to imperial
# if line contains metric, set mode to metric
# if line starts with x, create new hole. 
# 	if same line contains y, set y param of current hole. 
# 	if line doesn't contain y, use previous y value.
# if line starts with y, create new hole and use previous x value.
# if line contains M30, it's the end of the file.
# write NC code with detected hole positions!
import sys
inputname = sys.argv[1]
excellonFile = open(inputname, 'r')
imperial = False
xCoordinates = []
yCoordinates = []

plungeDepth = "-2.100000"
firstPlunge = "-2.10"

def cleanNumber(value):
	decimals = value[4:]
	number = value[:4]
	return number.lstrip("0") + "." + decimals

for line in excellonFile:
	if "INCH" in line:
		imperial = True
		print "Detected imperial units."
	if "METRIC" in line:
		imperial = False
		print "Detected metric units."
	if line.startswith('X'):
		if "Y" in line:
			print "Detected hole"
			xCoordinates.append(line[1:line.find('Y')])
			yCoordinates.append(line[line.find('Y')+1:].rstrip())
		else:
			print "Detected hole (X orphan)"
			xCoordinates.append(line[1:].rstrip())
			yCoordinates.append(yCoordinates[-1])
	if line.startswith('Y'):
		print "Detected hole (Y orphan)"
		xCoordinates.append(xCoordinates[-1])
		yCoordinates.append(line[1:].rstrip())
	if "M30" in line:
		print "End of Excellon file."
print xCoordinates
print "----------"
print yCoordinates

outputname = inputname[:-4] + ".nc"
ncFile = open(outputname, 'w')

# start of the file, start routine.
ncFile.write("G21")
ncFile.write("\n")
ncFile.write("G90")
ncFile.write("\n")
ncFile.write("M05")
ncFile.write("\n")
ncFile.write("G00 Z10.00")
ncFile.write("\n")
ncFile.write("G00 X0.00 Y0.00")
ncFile.write("\n")
ncFile.write("G01 Z0.00 F35.00")
ncFile.write("\n")
ncFile.write("G00 Z1.00")
ncFile.write("\n")
ncFile.write("M03")
ncFile.write("\n")
ncFile.write("G04 P 6")
ncFile.write("\n")
ncFile.write("G00 Z1.000000")
ncFile.write("\n")

firstHole = True

for x, y in zip(xCoordinates, yCoordinates):
	ncFile.write("G00 X" + cleanNumber(x) + " Y" + cleanNumber(y))
	ncFile.write("\n")
	ncFile.write("G01 Z" + plungeDepth)
	ncFile.write("\n")
	if firstHole is True:
		ncFile.write("G01 Z" + firstPlunge + " F35.00")
		ncFile.write("\n")
		firstHole = False
	else:
		ncFile.write("G01 Z" + plungeDepth)
		ncFile.write("\n")
	ncFile.write("G01 Z1.000000")
	ncFile.write("\n")

ncFile.write("T01")
ncFile.write("\n")
ncFile.write("G00 Z2.00")
ncFile.write("\n")
ncFile.write("M05")
ncFile.write("\n")
ncFile.write("M02")
ncFile.write("\n")

